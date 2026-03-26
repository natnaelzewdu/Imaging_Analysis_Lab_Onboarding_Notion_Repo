"""
Populate the 'Technical Onboarding' data source with tasks extracted
from the Imaging-Analysis Getting Started document.

Usage:
    python push_technical_tasks.py
"""

import time
from config import TECHNICAL_DATA_SOURCE_ID
from docx_parser import load_paragraphs, extract_description_by_range, extract_images
from notion_api import create_page, add_image_block, upload_image

DOCX_PATH = r"data\Imaging-Analysis Getting Started.docx"

TASKS = [
    {
        "task_name": "Read Technical Onboarding Introduction",
        "emoji": "👋",
        "para_range": (27, 42),
        "images": [
            {"ref": "media/image1.jpeg", "caption": "Imaging-Analysis Laboratory, TReNDS Center, Georgia State University"},
        ],
        "url": "https://scholar.google.com/citations?view_op=list_works&hl=en&hl=en&user=e35VA6sAAAAJ&sortby=pubdate",
    },
    {
        "task_name": "Set Up and Review TReNDS Computing Cluster",
        "emoji": "🖥️",
        "para_range": (43, 69),
        "images": [],
        "url": "https://trendscenter.github.io/wiki/docs/Getting_Started.html",
    },
    {
        "task_name": "Learn Independent Component Analysis (ICA)",
        "emoji": "🧠",
        "para_range": (70, 83),
        "images": [],
        "url": "https://doi.org/10.1016/j.neuroimage.2008.10.057",
    },
    {
        "task_name": "Identify and Label Brain Networks",
        "emoji": "🧩",
        "para_range": (84, 100),
        "images": [
            {"ref": "media/image2.png", "caption": "Spatial maps of 12 large-scale functional brain networks commonly obtained from sICA (From Iraji et al., 2019)"},
        ],
        "url": "https://doi.org/10.1002/hbm.24580",
    },
    {
        "task_name": "Learn Data Visualization Tools",
        "emoji": "📊",
        "para_range": (101, 135),
        "images": [
            {"ref": "media/image3.png", "caption": "GIFT Display Tools — select Image viewer from the central drop-down menu"},
            {"ref": "media/image4.png", "caption": "Select the images you wish to visualize"},
            {"ref": "media/image5.png", "caption": "Display options: display type, image Z-scoring, thresholding, and additional parameters"},
            {"ref": "media/image6.png", "caption": "GIFT displays chosen images according to the selected display parameters"},
            {"ref": "media/image7.png", "caption": "Suprathreshold-only display (left) vs. dual coded subthreshold and suprathreshold approach (right) — From Allen et al. (2012)"},
        ],
        "url": "https://doi.org/10.1016/j.neuron.2012.05.001",
    },
    {
        "task_name": "Explore TReNDS Databases and Resources",
        "emoji": "🗄️",
        "para_range": (136, 200),
        "images": [],
        "url": None,
    },
]


def main():
    paragraphs = load_paragraphs(DOCX_PATH)
    image_blobs = extract_images(DOCX_PATH)

    print(f"Creating {len(TASKS)} technical tasks...\n")

    for i, task in enumerate(TASKS, 1):
        start, end = task["para_range"]
        desc = extract_description_by_range(paragraphs, start, end)

        print(f"  [{i}/{len(TASKS)}] {task['emoji']} {task['task_name']} ({len(desc)} chars)")
        page_id = create_page(
            TECHNICAL_DATA_SOURCE_ID,
            task["task_name"],
            desc,
            emoji=task["emoji"],
            url=task.get("url"),
        )
        if not page_id:
            continue

        for img_entry in task.get("images", []):
            img_ref = img_entry["ref"]
            if img_ref not in image_blobs:
                continue
            img = image_blobs[img_ref]
            filename = img_ref.split("/")[-1]
            caption = img_entry.get("caption", "")
            print(f"    Image: {filename} — {caption}")
            fid = upload_image(img["blob"], filename, img["content_type"])
            if fid:
                time.sleep(1)
                add_image_block(page_id, fid, caption)
                time.sleep(2)

    print("\nDone!")


if __name__ == "__main__":
    main()
