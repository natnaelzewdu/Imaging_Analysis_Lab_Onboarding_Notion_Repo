"""
Populate the General Info data source with handbook tasks.
Now simplified to 2 tasks: handbook overview + meetings.

Usage:
    python push_handbook_tasks.py
"""

import os
from config import HANDBOOK_DATA_SOURCE_ID
from notion_api import create_page, query_data_source, archive_page, append_body_content

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content", "handbook")

TASKS = [
    {
        "task_name": "Read the Lab Handbook",
        "heading": "Welcome to Imaging-Analysis Lab!",
        "category": "Lab Culture & Conduct",
        "order": 1,
        "body_file": "00_read_lab_handbook.md",
    },
    {
        "task_name": "Conduct in Meetings",
        "heading": "Conduct in Meetings:",
        "category": "Lab Culture & Conduct",
        "order": 2,
        "body_file": "05_conduct_in_meetings.md",
    },
]

ICON_MAP = {
    "Read the Lab Handbook": "📖",
    "Conduct in Meetings": "🗣️",
}

IMAGE_MAP = {}  # No embedded docx images needed


def _get_emoji(task_name: str) -> str:
    for keyword, emoji in ICON_MAP.items():
        if keyword in task_name:
            return emoji
    return "📌"


def main(delete_first=False):
    # Optionally delete all existing handbook tasks
    existing = query_data_source(HANDBOOK_DATA_SOURCE_ID)
    if delete_first and existing:
        print(f"Archiving {len(existing)} existing tasks...")
        for name, page_id in existing.items():
            print(f"  \U0001f5d1\ufe0f  {name}")
            archive_page(page_id)
        print()
        existing = {}  # All deleted, none to skip

    # Deduplicate: skip tasks that already exist
    tasks_to_create = [t for t in TASKS if t["task_name"] not in existing]
    skipped = len(TASKS) - len(tasks_to_create)
    if skipped:
        print(f"Skipping {skipped} tasks that already exist.\n")

    print(f"Creating {len(tasks_to_create)} handbook tasks...\n")

    for i, task in enumerate(tasks_to_create, 1):
        emoji = _get_emoji(task["task_name"])
        print(f"  [{i}/{len(tasks_to_create)}] {emoji} {task['task_name']}")
        page_id = create_page(
            HANDBOOK_DATA_SOURCE_ID,
            task["task_name"],
            emoji=emoji,
            url=task.get("url"),
            category=task.get("category"),
            tier="Theory",
            order=task.get("order"),
        )
        if page_id and task.get("body_file"):
            body_path = os.path.join(CONTENT_DIR, task["body_file"])
            if os.path.exists(body_path):
                with open(body_path, "r", encoding="utf-8") as f:
                    body = f.read()
                append_body_content(page_id, body)
            else:
                print(f"    ⚠ Body file not found: {task['body_file']}")

    print("\nDone!")


if __name__ == "__main__":
    main()
