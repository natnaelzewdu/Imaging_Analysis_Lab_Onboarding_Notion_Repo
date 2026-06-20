"""
Populate the 'Tools & Workflows' data source with proposed tool categories.
These are placeholder entries — task names and content to be filled in.

Usage:
    python push_tools_tasks.py
"""

import os
from config import TOOLS_DATA_SOURCE_ID
from notion_api import create_page, query_data_source, archive_page, append_body_content

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content", "tools")

TASKS = [
    # --- Version Control ---
    {
        "task_name": "Git & GitHub Basics",
        "emoji": "🔀",
        "category": "Version Control & Coding Tools",
        "tier": "Hands-On",
        "order": 1,
        "url": "https://github.com/trendscenter",
        "body_file": "01_git_github.md",
    },
    # --- VS Code ---
    {
        "task_name": "VS Code for Remote Development",
        "emoji": "💻",
        "category": "Version Control & Coding Tools",
        "tier": "Hands-On",
        "order": 2,
        "url": "https://code.visualstudio.com/docs/remote/ssh",
        "body_file": "02_vscode.md",
    },
]


def main(delete_first=False):
    existing = query_data_source(TOOLS_DATA_SOURCE_ID)
    if delete_first and existing:
        print(f"Archiving {len(existing)} existing tasks...")
        for name, page_id in existing.items():
            print(f"  🗑️  {name}")
            archive_page(page_id)
        print()
        existing = {}

    tasks_to_create = [t for t in TASKS if t["task_name"] not in existing]
    skipped = len(TASKS) - len(tasks_to_create)
    if skipped:
        print(f"Skipping {skipped} tasks that already exist.\n")

    print(f"Creating {len(tasks_to_create)} tools & workflows tasks...\n")

    for i, task in enumerate(tasks_to_create, 1):
        print(f"  [{i}/{len(tasks_to_create)}] {task['emoji']} {task['task_name']}")
        page_id = create_page(
            TOOLS_DATA_SOURCE_ID,
            task["task_name"],
            emoji=task["emoji"],
            url=task.get("url"),
            category=task.get("category"),
            tier=task.get("tier"),
            order=task.get("order"),
        )
        if page_id and task.get("body_file"):
            body_path = os.path.join(CONTENT_DIR, task["body_file"])
            if os.path.exists(body_path):
                with open(body_path, "r", encoding="utf-8") as f:
                    body = f.read()
                append_body_content(page_id, body)

    print("\nDone!")


if __name__ == "__main__":
    main()
