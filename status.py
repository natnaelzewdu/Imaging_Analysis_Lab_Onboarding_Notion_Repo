"""
=============================================================================
CONTEXT FILE FOR NEXT CHAT SESSION
=============================================================================
Run this to see the current state of the project and what needs to be done.

Usage: python status.py
=============================================================================
"""

import os
import json

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content", "beginner")


def main():
    # Load all task definitions
    from push_beginner_tasks import TASKS

    print("=" * 70)
    print("NOTION ONBOARDING PROJECT — STATUS")
    print("=" * 70)

    print(f"\nTotal beginner tasks defined: {len(TASKS)}")
    print(f"Content directory: {CONTENT_DIR}\n")

    # Check which tasks have deep content files
    done = []
    todo = []
    for task in TASKS:
        body_file = task.get("body_file")
        if body_file:
            path = os.path.join(CONTENT_DIR, body_file)
            if os.path.exists(path):
                size = os.path.getsize(path)
                done.append((task["task_name"], body_file, size))
            else:
                todo.append((task["task_name"], body_file, "FILE MISSING"))
        else:
            # Needs a body_file entry + content written
            suggested = task["task_name"].lower().replace(" ", "_").replace("&", "and")
            suggested = suggested.replace("(", "").replace(")", "").replace("—", "")
            suggested = suggested.replace(",", "").replace("'", "").replace("/", "_")
            suggested = suggested.strip("_")
            todo.append((task["task_name"], f"XX_{suggested}.md", "NEEDS WRITING"))

    print(f"Tasks with deep content: {len(done)}/{len(TASKS)}")
    print(f"Tasks still needing deep content: {len(todo)}/{len(TASKS)}")

    if done:
        print("\n✅ COMPLETED:")
        for name, file, size in done:
            print(f"   {file} ({size:,} bytes) — {name}")

    if todo:
        print("\n📝 TODO (in recommended order):")
        for i, (name, file, status) in enumerate(todo, 1):
            tier = next(t["tier"] for t in TASKS if t["task_name"] == name)
            cat = next(t["category"] for t in TASKS if t["task_name"] == name)
            print(f"   {i:2d}. [{tier}] [{cat}] {name}")

    # Print the task structure for reference
    print("\n" + "=" * 70)
    print("FULL TASK LIST BY TIER → CATEGORY → ORDER")
    print("=" * 70)

    # Group by tier then category
    from collections import defaultdict
    by_tier = defaultdict(lambda: defaultdict(list))
    for t in TASKS:
        by_tier[t["tier"]][t["category"]].append(t)

    for tier in ["Theory", "Hands-On"]:
        print(f"\n{'─' * 35}")
        print(f"  TIER: {tier}")
        print(f"{'─' * 35}")
        for cat, tasks in sorted(by_tier[tier].items()):
            print(f"\n  📁 {cat}")
            for t in sorted(tasks, key=lambda x: x.get("order", 99)):
                has_file = "✅" if t.get("body_file") and os.path.exists(
                    os.path.join(CONTENT_DIR, t["body_file"])
                ) else "⬜"
                print(f"     {has_file} {t['order']:2d}. {t['emoji']} {t['task_name']}")

    # Instructions for the next session
    print("\n" + "=" * 70)
    print("WHAT TO DO NEXT")
    print("=" * 70)
    print("""
For each task that needs deep content:

1. Create a .md file in content/beginner/ with the naming pattern:
   XX_task_name_in_snake_case.md

2. Write deep content using this format:
   ## Heading          → becomes Notion heading_2
   ### Subheading      → becomes Notion heading_3
   - bullet item       → becomes Notion bulleted_list_item
   [link text](url)    → becomes clickable link in Notion
   plain text          → becomes Notion paragraph

3. Add "body_file": "XX_filename.md" to the task dict in push_beginner_tasks.py

4. Content guidelines (based on approved test page):
   - Teach the concept fully, don't just link to resources
   - Write as if explaining to a CS/engineering student new to neuroimaging
   - Include inline links naturally in the text: [MRI physics](https://...)
   - End with a "Resources for deeper learning" section with labeled links
   - NO "Check your understanding" / quiz sections
   - Connect each topic to the lab's work (ICA, brain networks, etc.)
   - Be detailed — the approved fMRI page was ~4000 chars

5. Test: python main.py --beginner
   (idempotent — skips existing tasks, only creates new ones)

NOTE: The 37 shallow versions already exist in Notion. To re-push with
deep content, you'll need to either:
  a) Delete existing tasks from Notion first, OR
  b) Add an --update mode that patches existing pages with body content
""")


if __name__ == "__main__":
    main()
