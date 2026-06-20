"""
Pull current page body content from Notion back to local .md files.

Reads task metadata from YAML frontmatter in each content/<tab>/*.md file,
fetches the matching Notion page blocks, converts them to Markdown, and
overwrites the body section of the local file (preserving frontmatter).

Also supports plain pages (content/<folder>/_page.yaml) — pulls the full
page body into the single .md file in that folder.

Usage:
    python pull_notion.py               # pull all tabs + plain pages
    python pull_notion.py --tab technical_onboarding   # pull one tab
    python pull_notion.py --tab welcome                # pull the Welcome page
    python pull_notion.py --dry-run     # show what would change, don't write
"""
import os
import sys
import re

import yaml

from notion_api import _request

CONTENT_ROOT = os.path.join(os.path.dirname(__file__), "content")
DRY_RUN = "--dry-run" in sys.argv
TAB_ARG = next(
    (sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--tab" and i + 1 < len(sys.argv)),
    None,
)


def _load_config() -> object:
    import importlib
    return importlib.import_module("config")


def discover_tabs() -> dict[str, str]:
    """Return {folder_name: data_source_id} from _tab.yaml files."""
    config_mod = _load_config()
    tabs: dict[str, str] = {}
    for entry in sorted(os.listdir(CONTENT_ROOT)):
        tab_dir = os.path.join(CONTENT_ROOT, entry)
        cfg_file = os.path.join(tab_dir, "_tab.yaml")
        if not os.path.isdir(tab_dir) or not os.path.isfile(cfg_file):
            continue
        with open(cfg_file, encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        env_var = cfg.get("notion_env_var")
        if not env_var:
            continue
        ds_id = getattr(config_mod, env_var, None) or os.environ.get(env_var)
        if ds_id:
            tabs[entry] = ds_id
    return tabs


def discover_pages() -> dict[str, str]:
    """Return {folder_name: page_id} from _page.yaml files."""
    config_mod = _load_config()
    pages: dict[str, str] = {}
    for entry in sorted(os.listdir(CONTENT_ROOT)):
        page_dir = os.path.join(CONTENT_ROOT, entry)
        cfg_file = os.path.join(page_dir, "_page.yaml")
        if not os.path.isdir(page_dir) or not os.path.isfile(cfg_file):
            continue
        with open(cfg_file, encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        env_var = cfg.get("notion_env_var")
        if not env_var:
            continue
        page_id = getattr(config_mod, env_var, None) or os.environ.get(env_var)
        if page_id:
            pages[entry] = page_id
    return pages


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


# ── Pull a single tab ──────────────────────────────────────────────────────

def _parse_frontmatter(filepath: str) -> tuple[dict | None, str]:
    """Return (meta, raw_frontmatter_block) from an .md file."""
    with open(filepath, encoding="utf-8") as fh:
        raw = fh.read()
    if not raw.startswith("---"):
        return None, ""
    parts = raw.split("---", 2)
    if len(parts) < 3:
        return None, ""
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return None, ""
    return meta, "---" + parts[1] + "---"


def pull_tab(tab_key: str, data_source_id: str, dry_run: bool = False) -> None:
    tab_dir = os.path.join(CONTENT_ROOT, tab_key)
    if not os.path.isdir(tab_dir):
        print(f"  Directory not found: {tab_dir}")
        return

    print(f"\n{'='*60}")
    print(f"Pulling: {tab_key}")
    print(f"{'='*60}")

    # Query Notion for task_name → page_id
    r = _request("post", f"data_sources/{data_source_id}/query", json={"page_size": 100})
    if r.status_code != 200:
        print(f"  Error querying data source: {r.status_code}")
        return

    name_to_id: dict[str, str] = {}
    for page in r.json().get("results", []):
        title_arr = page["properties"].get("Task Name", {}).get("title", [])
        if title_arr:
            name_to_id[title_arr[0]["plain_text"]] = page["id"]

    for root, _dirs, files in os.walk(tab_dir):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
        meta, fm_block = _parse_frontmatter(fpath)
        if not meta or not meta.get("task_name"):
            continue

        task_name = meta["task_name"]
        if task_name not in name_to_id:
            print(f"  ⚠ Not found in Notion: {task_name}")
            continue

        page_id = name_to_id[task_name]
        blocks = fetch_blocks(page_id)
        if not blocks:
            print(f"  (empty body in Notion) {task_name}")
            continue

        body_md = blocks_to_md(blocks)

        if dry_run:
            print(f"  [dry-run] {task_name} — {len(body_md)} chars → {fname}")
            continue

        # Preserve the frontmatter, replace the body
        with open(fpath, "w", encoding="utf-8") as fh:
            fh.write(fm_block + "\n" + body_md + "\n")
        print(f"  ✓ {task_name} → {fname}")


# ── Pull a plain Notion page ────────────────────────────────────────────────

def pull_page(folder_key: str, page_id: str, dry_run: bool = False) -> None:
    """Pull a plain Notion page's blocks into the single .md file in folder."""
    folder = os.path.join(CONTENT_ROOT, folder_key)

    print(f"\n{'='*60}")
    print(f"Pulling plain page: {folder_key}")
    print(f"{'='*60}")

    blocks = fetch_blocks(page_id)
    if not blocks:
        print("  Page is empty in Notion.")
        return

    body_md = blocks_to_md(blocks)

    # Find the .md file to write to (first one found, or create default)
    md_files = [f for f in os.listdir(folder) if f.endswith(".md")]
    target = os.path.join(folder, md_files[0] if md_files else f"{folder_key}.md")

    if dry_run:
        print(f"  [dry-run] Would write {len(body_md)} chars → {os.path.basename(target)}")
        return

    with open(target, "w", encoding="utf-8") as fh:
        fh.write(body_md + "\n")
    print(f"  ✓ {folder_key} → {os.path.basename(target)}")


# ── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if DRY_RUN:
        print("DRY RUN — no files will be written\n")

    tabs = discover_tabs()
    pages = discover_pages()
    all_folders = {**tabs, **pages}

    if TAB_ARG and TAB_ARG not in all_folders:
        print(f"Unknown folder '{TAB_ARG}'. Valid options: {', '.join(all_folders)}")
        sys.exit(1)

    if TAB_ARG:
        if TAB_ARG in pages:
            pull_page(TAB_ARG, pages[TAB_ARG], dry_run=DRY_RUN)
        else:
            pull_tab(TAB_ARG, tabs[TAB_ARG], dry_run=DRY_RUN)
    else:
        for folder_key, page_id in pages.items():
            pull_page(folder_key, page_id, dry_run=DRY_RUN)
        for tab_key, ds_id in tabs.items():
            pull_tab(tab_key, ds_id, dry_run=DRY_RUN)

    print("\nPull complete.")
