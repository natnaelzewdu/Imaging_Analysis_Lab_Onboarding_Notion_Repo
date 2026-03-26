"""
Populate the 'Nate Onboarding Track' (Trends Onboarding) data source
with tasks extracted from the Imaging-Analysis Lab Handbook.

Usage:
    python push_handbook_tasks.py
"""

import time
from config import HANDBOOK_DATA_SOURCE_ID
from docx_parser import load_paragraphs, extract_description_by_heading, extract_images
from notion_api import create_page, add_image_block, upload_image

DOCX_PATH = r"data\Imaging-Analysis Lab Handbook.docx"

# Each task maps to a heading in the handbook.
# All stop_headings are collected once and shared across all tasks.
SECTION_STOP_HEADINGS = [
    "Workplace Conduct",
    "Work and Wellbeing",
    "Equality, Diversion",
    "Career Development",
    "Open & Responsible Science",
    "Collaborating",
    "Travel and Conferences",
    "Taking care of your",
]

TASKS = [
    {"task_name": "Read Lab Introduction", "heading": "Welcome to Imaging-Analysis Lab!"},
    {"task_name": "Review Student Role & Expectations", "heading": "Students:"},
    {"task_name": "Review Postdoc Role", "heading": "Postdoctoral Researchers (Postdocs):"},
    {"task_name": "Review PI Role", "heading": "Principal Investigator (PI):"},
    {"task_name": "Review Conduct in Meetings", "heading": "Conduct in Meetings:"},
    {"task_name": "Review Office Interaction Guidelines", "heading": "Office Interaction Guidelines:"},
    {"task_name": "Review Socializing Guidelines", "heading": "Socializing:"},
    {
        "task_name": "Review Inappropriate Behavior Policy",
        "heading": "Addressing Inappropriate Behavior:",
        "url": "https://victimassistance.gsu.edu/information-facultysestaff-member/",
    },
    {"task_name": "Review Setting Clear Expectations", "heading": "Setting Clear Expectations:"},
    {"task_name": "Review Balancing Working Hours", "heading": "Balancing Working Hours:"},
    {"task_name": "Review Work and Personal Life", "heading": "Work and Personal Life:"},
    {"task_name": "Review Mental Wellbeing Resources", "heading": "Prioritizing Mental Wellbeing:"},
    {"task_name": "Review Equality, Diversity & Inclusion", "heading": "At our lab, we are fully committed"},
    {"task_name": "Review Building Your CV", "heading": "Building Your CV:"},
    {"task_name": "Create Individual Development Plan (IDP)", "heading": "Individual Development Plan (IDP):"},
    {"task_name": "Prepare for Annual Evaluations", "heading": "Annual Evaluations:"},
    {"task_name": "Review Open Science Practices", "heading": "Open Science:"},
    {"task_name": "Review Reproducible Research", "heading": "Reproducible Research:"},
    {"task_name": "Review Discovering Mistakes", "heading": "Discovering Mistakes:"},
    {"task_name": "Review Research Conduct & Ethics", "heading": "Research Conduct:"},
    {"task_name": "Review Collaboration Guidelines", "heading": "Why collaborate?"},
    {"task_name": "Review Collaboration Expectations", "heading": "Setting Expectations: It is important to be clear"},
    {"task_name": "Review Conferences Overview", "heading": "Conferences Overview:"},
    {"task_name": "Review Poster Printing Procedures", "heading": "Poster Printing:"},
    {"task_name": "Review Conference Expectations & Logistics", "heading": "Expectations and Logistics:"},
]

ICON_MAP = {
    "Read Lab Introduction": "👋", "Student Role": "🎓", "Postdoc Role": "🔬",
    "PI Role": "👨‍🏫", "Conduct in Meetings": "🗣️", "Office Interaction": "🏢",
    "Socializing": "☕", "Inappropriate Behavior": "🛡️",
    "Setting Clear Expectations": "🎯", "Balancing Working Hours": "⏰",
    "Work and Personal Life": "⚖️", "Mental Wellbeing": "🧠",
    "Equality, Diversity": "🌍", "Building Your CV": "📄",
    "Individual Development Plan": "📋", "Annual Evaluations": "📊",
    "Open Science": "🔓", "Reproducible Research": "🔁",
    "Discovering Mistakes": "🔍", "Research Conduct": "⚖️",
    "Collaboration Guidelines": "🤝", "Collaboration Expectations": "📝",
    "Conferences Overview": "🎤", "Poster Printing": "🖨️",
    "Conference Expectations": "✈️",
}

# Image mapping: docx image ref -> task name + caption
IMAGE_MAP = {
    "../media/image.jpg": {
        "task_name": "Read Lab Introduction",
        "caption": "Imaging-Analysis Laboratory",
    },
}


def _get_emoji(task_name: str) -> str:
    for keyword, emoji in ICON_MAP.items():
        if keyword in task_name:
            return emoji
    return "📌"


def main():
    paragraphs = load_paragraphs(DOCX_PATH)

    # Build stop headings: all task headings + section headers
    all_headings = [t["heading"] for t in TASKS] + SECTION_STOP_HEADINGS

    print(f"Creating {len(TASKS)} handbook tasks...\n")

    # Track created pages for image attachment
    page_ids: dict[str, str] = {}

    for i, task in enumerate(TASKS, 1):
        stop = [h for h in all_headings if h != task["heading"]]
        desc = extract_description_by_heading(paragraphs, task["heading"], stop)
        emoji = _get_emoji(task["task_name"])

        print(f"  [{i}/{len(TASKS)}] {emoji} {task['task_name']} ({len(desc)} chars)")
        page_id = create_page(
            HANDBOOK_DATA_SOURCE_ID,
            task["task_name"],
            desc,
            emoji=emoji,
            url=task.get("url"),
        )
        if page_id:
            page_ids[task["task_name"]] = page_id

    # Attach images
    images = extract_images(DOCX_PATH)
    for img_ref, img_info in IMAGE_MAP.items():
        if img_ref not in images:
            continue
        task_name = img_info["task_name"]
        if task_name not in page_ids:
            continue
        img = images[img_ref]
        filename = img_ref.split("/")[-1]
        print(f"\n  Uploading {filename} -> {task_name}")
        fid = upload_image(img["blob"], filename, img["content_type"])
        if fid:
            time.sleep(1)
            add_image_block(page_ids[task_name], fid, img_info.get("caption", ""))

    print("\nDone!")


if __name__ == "__main__":
    main()
