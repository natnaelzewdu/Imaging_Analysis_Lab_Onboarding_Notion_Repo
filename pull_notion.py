"""
Pull current page body content from Notion back to local .md files.

Fetches blocks for every task that has a body_file, converts them to
the same markdown-like format that append_body_content() reads, and
overwrites the local file.

Usage:
    python pull_notion.py               # pull all data sources
    python pull_notion.py --dry-run     # show what would change, don't write
"""
import os
import sys
import re
from notion_api import _request
from config import (
    TECHNICAL_DATA_SOURCE_ID, HANDBOOK_DATA_SOURCE_ID,
    TOOLS_DATA_SOURCE_ID, FUNDING_DATA_SOURCE_ID,
)

DRY_RUN = "--dry-run" in sys.argv

# ── Rich-text array → markdown string ──────────────────────────────────────

def rt_to_md(rich_text: list) -> str:
    result = ""
    for rt in rich_text:
        text = rt.get("plain_text", "")
        if not text:
            continue
        ann = rt.get("annotations", {})
        href = (rt.get("href")
                or (rt.get("text", {}).get("link") or {}).get("url"))
        if ann.get("bold") and href:
            text = f"**[{text}]({href})**"
        elif ann.get("bold"):
            text = f"**{text}**"
        elif href:
            text = f"[{text}]({href})"
        elif ann.get("italic"):
            text = f"*{text}*"
        elif ann.get("code"):
            text = f"`{text}`"
        result += text
    return result


# ── Fetch all blocks for a page (handles pagination) ───────────────────────

def fetch_blocks(page_id: str) -> list:
    blocks = []
    cursor = None
    while True:
        params = {"page_size": 100}
        if cursor:
            params["start_cursor"] = cursor
        r = _request("get", f"blocks/{page_id}/children", params=params)
        if r.status_code != 200:
            print(f"    Error fetching blocks: {r.status_code}")
            break
        data = r.json()
        blocks.extend(data.get("results", []))
        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")
    return blocks


# ── Blocks → markdown ───────────────────────────────────────────────────────

def blocks_to_md(blocks: list) -> str:
    lines = []
    in_numbered = False

    for b in blocks:
        btype = b.get("type", "")
        content = b.get(btype, {})

        if btype in ("heading_1",):
            text = rt_to_md(content.get("rich_text", []))
            lines.append(f"# {text}")

        elif btype == "heading_2":
            text = rt_to_md(content.get("rich_text", []))
            lines.append(f"## {text}")

        elif btype == "heading_3":
            text = rt_to_md(content.get("rich_text", []))
            lines.append(f"### {text}")

        elif btype == "bulleted_list_item":
            text = rt_to_md(content.get("rich_text", []))
            lines.append(f"- {text}")

        elif btype == "numbered_list_item":
            text = rt_to_md(content.get("rich_text", []))
            lines.append(f"1. {text}")

        elif btype == "paragraph":
            text = rt_to_md(content.get("rich_text", []))
            lines.append(text)  # empty string for blank lines is fine

        elif btype == "code":
            lang = content.get("language", "plain text")
            code = content.get("rich_text", [{}])[0].get("plain_text", "") if content.get("rich_text") else ""
            lines.append(f"```{lang}\n{code}\n```")

        elif btype == "image":
            img = content
            caption = rt_to_md(img.get("caption", []))
            img_type = img.get("type", "")
            if img_type == "external":
                url = img.get("external", {}).get("url", "")
                lines.append(f"![{caption}]({url})")
            elif img_type == "file":
                url = img.get("file", {}).get("url", "")
                lines.append(f"![{caption}]({url})")
            elif img_type == "file_upload":
                # Uploaded files — can't round-trip to local path
                lines.append(f"<!-- uploaded image: {caption} -->")

        elif btype == "divider":
            lines.append("---")

        elif btype in ("callout", "quote"):
            text = rt_to_md(content.get("rich_text", []))
            lines.append(f"> {text}")

        elif btype == "table_of_contents":
            pass  # skip

        elif btype == "table":
            pass  # skip complex tables

        # Child blocks (e.g. toggle, column) — recurse if has_children
        if b.get("has_children") and btype not in ("table",):
            child_blocks = fetch_blocks(b["id"])
            if child_blocks:
                lines.append(blocks_to_md(child_blocks))

    # Join, collapsing more than 2 consecutive blank lines to 1
    text = "\n\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ── Pull a single data source ───────────────────────────────────────────────

def pull_data_source(data_source_id: str, tasks: list, content_dir: str, label: str):
    print(f"\n{'='*60}")
    print(f"Pulling: {label}")
    print(f"{'='*60}")

    r = _request("post", f"data_sources/{data_source_id}/query", json={"page_size": 100})
    if r.status_code != 200:
        print(f"  Error querying data source: {r.status_code}")
        return

    # Build name → page_id map
    name_to_id: dict[str, str] = {}
    for page in r.json().get("results", []):
        title_arr = page["properties"].get("Task Name", {}).get("title", [])
        if title_arr:
            name_to_id[title_arr[0]["plain_text"]] = page["id"]

    for task in tasks:
        body_file = task.get("body_file")
        if not body_file:
            continue
        task_name = task["task_name"]
        if task_name not in name_to_id:
            print(f"  ⚠ Not found in Notion: {task_name}")
            continue

        page_id = name_to_id[task_name]
        blocks = fetch_blocks(page_id)
        if not blocks:
            print(f"  (empty) {task_name}")
            continue

        md = blocks_to_md(blocks)

        # Resolve file path (handle ../tools/ style relative refs)
        file_path = os.path.normpath(os.path.join(content_dir, body_file))

        if DRY_RUN:
            print(f"  [dry-run] Would write {len(md)} chars -> {os.path.relpath(file_path)}")
            continue

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md + "\n")
        print(f"  ✓ {task_name} → {os.path.relpath(file_path)}")


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import push_beginner_tasks
    import push_technical_tasks
    import push_handbook_tasks
    import push_tools_tasks
    import push_funding_tasks

    BEGINNER_DIR = os.path.join(os.path.dirname(__file__), "content", "beginner")
    HANDBOOK_DIR = os.path.join(os.path.dirname(__file__), "content", "handbook")
    TOOLS_DIR    = os.path.join(os.path.dirname(__file__), "content", "tools")
    FUNDING_DIR  = os.path.join(os.path.dirname(__file__), "content", "funding")

    if DRY_RUN:
        print("DRY RUN — no files will be written\n")

    # Beginner tasks (shared TECHNICAL_DATA_SOURCE_ID)
    pull_data_source(
        TECHNICAL_DATA_SOURCE_ID,
        [t for t in push_beginner_tasks.TASKS if t.get("body_file")],
        BEGINNER_DIR,
        "Foundations & Setup (beginner)",
    )

    # Handbook
    pull_data_source(
        HANDBOOK_DATA_SOURCE_ID,
        [t for t in push_handbook_tasks.TASKS if t.get("body_file")],
        HANDBOOK_DIR,
        "General Info (handbook)",
    )

    # Tools
    pull_data_source(
        TOOLS_DATA_SOURCE_ID,
        [t for t in push_tools_tasks.TASKS if t.get("body_file")],
        TOOLS_DIR,
        "Tools & Workflows",
    )

    # Funding
    pull_data_source(
        FUNDING_DATA_SOURCE_ID,
        [t for t in push_funding_tasks.TASKS if t.get("body_file")],
        FUNDING_DIR,
        "Funding & Fellowships",
    )

    print("\nSync complete.")
