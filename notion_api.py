"""Shared Notion API helpers — single source of truth for all API interactions."""

import time
import requests
from config import (
    NOTION_TOKEN,
    NOTION_API_VERSION,
    NOTION_BASE_URL,
    REQUEST_TIMEOUT,
    RATE_LIMIT_DELAY,
)

MAX_RICH_TEXT_LENGTH = 2000
MAX_RETRIES = 3


def create_session() -> requests.Session:
    """Create a configured requests session for the Notion API."""
    s = requests.Session()
    s.headers.update({
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_API_VERSION,
        "Content-Type": "application/json",
    })
    return s


_session = create_session()


def _request(method: str, path: str, **kwargs) -> requests.Response:
    """Make a rate-limited request to the Notion API."""
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)
    url = f"{NOTION_BASE_URL}/{path.lstrip('/')}"
    resp = getattr(_session, method)(url, **kwargs)
    time.sleep(RATE_LIMIT_DELAY)
    return resp


def query_data_source(data_source_id: str) -> dict[str, str]:
    """Query pages from a data source. Returns {task_name: page_id}."""
    resp = _request("post", f"data_sources/{data_source_id}/query", json={})
    resp.raise_for_status()
    pages = {}
    for page in resp.json().get("results", []):
        title_arr = page["properties"]["Task Name"]["title"]
        if title_arr:
            pages[title_arr[0]["plain_text"]] = page["id"]
    return pages


def create_page(
    data_source_id: str,
    task_name: str,
    emoji: str = "📌",
    url: str | None = None,
    category: str | None = None,
    tier: str | None = None,
    order: int | None = None,
) -> str | None:
    """Create a task page in a data source. Returns the page ID or None."""
    properties = {
        "Task Name": {"title": [{"text": {"content": task_name}}]},
        "Status": {"status": {"name": "Not started"}},
    }
    if url:
        properties["URL"] = {"url": url}
    if category:
        properties["Category"] = {"select": {"name": category}}
    if tier:
        properties["Tier"] = {"select": {"name": tier}}
    if order is not None:
        properties["Order"] = {"number": order}

    payload = {
        "parent": {"type": "data_source_id", "data_source_id": data_source_id},
        "icon": {"type": "emoji", "emoji": emoji},
        "properties": properties,
    }
    resp = _request("post", "pages", json=payload)
    if resp.status_code != 200:
        print(f"  Error creating page: {resp.status_code} {resp.text[:200]}")
        return None
    return resp.json()["id"]


def archive_page(page_id: str) -> bool:
    """Archive (soft-delete) a page by moving it to trash."""
    resp = _request("patch", f"pages/{page_id}", json={"in_trash": True})
    if resp.status_code != 200:
        print(f"  Error archiving page {page_id[:8]}: {resp.status_code} {resp.text[:200]}")
        return False
    return True


def set_page_icon(page_id: str, emoji: str) -> bool:
    """Set an emoji icon on a page."""
    resp = _request(
        "patch",
        f"pages/{page_id}",
        json={"icon": {"type": "emoji", "emoji": emoji}},
    )
    return resp.status_code == 200


def _parse_rich_text(text: str) -> list[dict]:
    """Parse text with inline formatting into Notion rich_text array.

    Supports:
      **bold text**        -> bold annotation
      [label](url)         -> clickable link
      **[label](url)**     -> bold clickable link
      Everything else      -> plain text
    """
    import re
    parts = []
    # Match bold-link, bold, or link tokens; everything else is plain text
    pattern = re.compile(
        r'\*\*\[([^\]]+)\]\(([^)]+)\)\*\*'   # **[label](url)**
        r'|\*\*([^*]+)\*\*'                    # **bold**
        r'|\[([^\]]+)\]\(([^)]+)\)'            # [label](url)
    )
    last_end = 0
    for m in pattern.finditer(text):
        # Plain text before this match
        if m.start() > last_end:
            parts.append({"type": "text", "text": {"content": text[last_end:m.start()]}})
        if m.group(1) is not None:
            # **[label](url)** — bold link
            parts.append({
                "type": "text",
                "text": {"content": m.group(1), "link": {"url": m.group(2)}},
                "annotations": {"bold": True},
            })
        elif m.group(3) is not None:
            # **bold**
            parts.append({
                "type": "text",
                "text": {"content": m.group(3)},
                "annotations": {"bold": True},
            })
        elif m.group(4) is not None:
            # [label](url)
            parts.append({
                "type": "text",
                "text": {"content": m.group(4), "link": {"url": m.group(5)}},
            })
        last_end = m.end()
    if last_end < len(text):
        parts.append({"type": "text", "text": {"content": text[last_end:]}})
    return parts if parts else [{"type": "text", "text": {"content": text}}]


def append_body_content(page_id: str, markdown_text: str, base_dir: str | None = None) -> bool:
    """Append rich content blocks to a page body from a simple markdown-like format.

    Supports:
      ## Heading       -> heading_2 block
      ### Heading      -> heading_3 block
      - item           -> bulleted_list_item block
      **bold**         -> bold text annotation
      [label](url)     -> inline links in any block
      ![caption](url)  -> external image block
      ```lang ... ```  -> code block
      Everything else  -> paragraph block
      Empty lines      -> skipped
    """
    import re
    import os
    import mimetypes
    lines = markdown_text.split("\n")
    children = []
    image_pattern = re.compile(r'^!\[([^\]]*)\]\(([^)]+)\)$')

    # State for fenced code blocks
    in_code_block = False
    code_lines: list[str] = []
    code_lang = "plain text"

    for line in lines:
        raw_stripped = line.strip()

        # --- Handle fenced code blocks ---
        if raw_stripped.startswith("```"):
            if not in_code_block:
                # Opening fence: ```python or ```bash or just ```
                in_code_block = True
                code_lines = []
                lang_hint = raw_stripped[3:].strip().lower()
                lang_map = {
                    "python": "python", "py": "python",
                    "matlab": "matlab", "m": "matlab",
                    "bash": "shell", "sh": "shell", "shell": "shell",
                    "r": "r", "json": "json", "yaml": "yaml",
                    "": "__auto__",
                }
                code_lang = lang_map.get(lang_hint, "plain text")
                continue
            else:
                # Closing fence
                in_code_block = False
                code_content = "\n".join(code_lines)
                # Auto-detect language if not specified
                if code_lang == "__auto__":
                    if any(kw in code_content for kw in ["function ", "addpath(", "fprintf(", "matlabbatch", "spm_", "spm(", "end\n", ">> "]):
                        code_lang = "matlab"
                    elif any(kw in code_content for kw in ["import ", "def ", "print(", "np.", "plt.", "pd.", "from "]):
                        code_lang = "python"
                    elif any(kw in code_content for kw in ["#SBATCH", "#!/bin/bash", "module load", "sbatch ", "srun ", "conda ", "pip ", "git ", "mkdir ", "cd ", "ls ", "ssh ", "scp ", "rsync ", "tar ", "echo ", "export ", "source ", "chmod "]):
                        code_lang = "shell"
                    else:
                        code_lang = "shell"
                # Notion code block rich_text max is 2000 chars
                if len(code_content) > 2000:
                    code_content = code_content[:2000]
                children.append({
                    "type": "code",
                    "code": {
                        "rich_text": [{"type": "text", "text": {"content": code_content}}],
                        "language": code_lang,
                    },
                })
                continue

        if in_code_block:
            code_lines.append(line.rstrip())
            continue

        # --- Normal line processing ---
        stripped = raw_stripped
        if not stripped:
            continue
        # Check for image line: ![caption](url)
        img_match = image_pattern.match(stripped)
        if img_match:
            caption_text = img_match.group(1)
            img_url = img_match.group(2)
            if img_url.startswith("local:"):
                # Local file -> upload to Notion and embed as a file_upload block.
                # Path is resolved relative to base_dir (or the repo root).
                rel = img_url[len("local:"):].strip()
                base = base_dir or os.path.dirname(os.path.abspath(__file__))
                local_path = rel if os.path.isabs(rel) else os.path.join(base, rel)
                if not os.path.isfile(local_path):
                    print(f"    Local image not found: {local_path}")
                    continue
                with open(local_path, "rb") as fh:
                    blob = fh.read()
                ctype = mimetypes.guess_type(local_path)[0] or "image/jpeg"
                file_id = upload_image(blob, os.path.basename(local_path), ctype)
                if not file_id:
                    print(f"    Upload failed for {os.path.basename(local_path)}")
                    continue
                image_block: dict = {
                    "type": "image",
                    "image": {"type": "file_upload", "file_upload": {"id": file_id}},
                }
            else:
                image_block = {
                    "type": "image",
                    "image": {
                        "type": "external",
                        "external": {"url": img_url},
                    },
                }
            if caption_text:
                image_block["image"]["caption"] = [
                    {"type": "text", "text": {"content": caption_text}}
                ]
            children.append(image_block)
        elif stripped.startswith("### "):
            children.append({
                "type": "heading_3",
                "heading_3": {"rich_text": _parse_rich_text(stripped[4:])},
            })
        elif stripped.startswith("## "):
            children.append({
                "type": "heading_2",
                "heading_2": {"rich_text": _parse_rich_text(stripped[3:])},
            })
        elif stripped.startswith("- "):
            children.append({
                "type": "bulleted_list_item",
                "bulleted_list_item": {"rich_text": _parse_rich_text(stripped[2:])},
            })
        else:
            children.append({
                "type": "paragraph",
                "paragraph": {"rich_text": _parse_rich_text(stripped)},
            })

    # Notion API allows max 100 blocks per request
    for i in range(0, len(children), 100):
        batch = children[i:i + 100]
        resp = _request("patch", f"blocks/{page_id}/children", json={"children": batch})
        if resp.status_code != 200:
            print(f"    Error appending body: {resp.status_code} {resp.text[:200]}")
            return False
    return True


def upload_image(image_blob: bytes, filename: str, content_type: str) -> str | None:
    """Upload an image to Notion. Returns the file_upload_id or None."""
    for attempt in range(MAX_RETRIES):
        try:
            cr = _request(
                "post",
                "file_uploads",
                json={
                    "mode": "single_part",
                    "filename": filename,
                    "content_type": content_type,
                },
            )
            if cr.status_code != 200:
                print(f"    Upload create error: {cr.status_code}")
                return None
            file_id = cr.json()["id"]

            time.sleep(1)

            # File send requires multipart — use raw requests (no JSON header)
            sr = requests.post(
                f"{NOTION_BASE_URL}/file_uploads/{file_id}/send",
                headers={
                    "Authorization": f"Bearer {NOTION_TOKEN}",
                    "Notion-Version": NOTION_API_VERSION,
                },
                files={"file": (filename, image_blob, content_type)},
                timeout=REQUEST_TIMEOUT,
            )
            if sr.status_code != 200:
                print(f"    Upload send error: {sr.status_code}")
                return None
            return file_id

        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            print(f"    Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep((attempt + 1) * 5)
    return None


def ensure_database_properties(data_source_id: str) -> bool:
    """Add Category, Tier, and Order properties to a data source if missing."""
    props = {
        "Category": {"select": {"options": []}},
        "Tier": {"select": {"options": [
            {"name": "Theory", "color": "blue"},
            {"name": "Hands-On", "color": "green"},
        ]}},
        "Order": {"number": {"format": "number"}},
    }
    resp = _request("patch", f"data_sources/{data_source_id}", json={"properties": props})
    if resp.status_code != 200:
        print(f"  Error updating properties: {resp.status_code} {resp.text[:300]}")
        return False
    print(f"  Properties ensured on data source {data_source_id[:8]}...")
    return True


def set_category_order(data_source_id: str, categories: list[str]) -> bool:
    """Patch the Category select options in the desired display order.

    Notion shows grouped-by-select categories in the order the options are
    defined on the property. To reorder existing options you must supply their
    existing IDs — otherwise Notion ignores the order. This function queries
    pages first to build a name→id map, then patches with the full ordered list.
    """
    # Step 1: collect existing option IDs from live pages
    resp = _request("post", f"data_sources/{data_source_id}/query", json={"page_size": 100})
    name_to_id: dict[str, str] = {}
    if resp.status_code == 200:
        for page in resp.json().get("results", []):
            cat = page["properties"].get("Category", {})
            if cat.get("type") == "select" and cat.get("select"):
                opt = cat["select"]
                if opt.get("id"):
                    name_to_id[opt["name"]] = opt["id"]

    # Step 2: build ordered options, include id for existing ones
    options = []
    for name in categories:
        opt: dict = {"name": name}
        if name in name_to_id:
            opt["id"] = name_to_id[name]
        options.append(opt)

    # Step 3: patch
    props = {"Category": {"select": {"options": options}}}
    resp = _request("patch", f"data_sources/{data_source_id}", json={"properties": props})
    if resp.status_code != 200:
        print(f"  Error setting category order: {resp.status_code} {resp.text[:300]}")
        return False
    print(f"  Category order set on {data_source_id[:8]}...")
    return True


def add_image_block(page_id: str, file_upload_id: str, caption: str = "") -> bool:
    """Append an image block (with optional caption) to a page."""
    image_block: dict = {
        "type": "image",
        "image": {
            "type": "file_upload",
            "file_upload": {"id": file_upload_id},
        },
    }
    if caption:
        image_block["image"]["caption"] = [
            {"type": "text", "text": {"content": caption}}
        ]
    resp = _request(
        "patch",
        f"blocks/{page_id}/children",
        json={"children": [image_block]},
    )
    return resp.status_code == 200
