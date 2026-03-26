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
    description: str,
    emoji: str = "📌",
    url: str | None = None,
) -> str | None:
    """Create a task page in a data source. Returns the page ID or None."""
    properties = {
        "Task Name": {"title": [{"text": {"content": task_name}}]},
        "Description": {
            "rich_text": [
                {"text": {"content": description[:MAX_RICH_TEXT_LENGTH]}}
            ]
        },
        "Status": {"status": {"name": "Not started"}},
        "Nate Status": {"status": {"name": "Not started"}},
    }
    if url:
        properties["URL"] = {"url": url}

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


def set_page_icon(page_id: str, emoji: str) -> bool:
    """Set an emoji icon on a page."""
    resp = _request(
        "patch",
        f"pages/{page_id}",
        json={"icon": {"type": "emoji", "emoji": emoji}},
    )
    return resp.status_code == 200


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
