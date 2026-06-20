"""
Populate beginner-friendly onboarding tasks covering all 13 categories.
Task metadata is defined inline. Deep body content is loaded from text files
in content/beginner/ directory.

Theory tasks should be completed before Hands-On tasks.

Usage:
    python push_beginner_tasks.py
"""

import os
from config import TECHNICAL_DATA_SOURCE_ID
from notion_api import create_page, query_data_source, append_body_content, archive_page

CONTENT_DIR = os.path.join(os.path.dirname(__file__), "content", "beginner")

# ---------------------------------------------------------------------------
# All beginner tasks organised by tier → category → order
# ---------------------------------------------------------------------------

TASKS = [
    # ======================================================================
    # TIER: Theory  (complete these first)
    # ======================================================================

    # ----- Research Foundations -----
    {
        "task_name": "Understand What fMRI Measures",
        "emoji": "🧲",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 1,
        "url": "https://www.youtube.com/watch?v=djAxjtN_7VE",
        "body_file": "01_understand_what_fmri_measures.md",
    },
    {
        "task_name": "Learn Basic Brain Anatomy for Neuroimaging",
        "emoji": "🧠",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 2,
        "url": "https://neurosynth.org/",
        "body_file": "38_learn_basic_brain_anatomy.md",
    },
    {
        "task_name": "Learn What ICA Is and Why It Matters",
        "emoji": "📊",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 3,
        "url": "https://doi.org/10.1016/j.neuroimage.2008.10.057",
        "body_file": "02_learn_what_ica_is_and_why_it_matters.md",
    },
    {
        "task_name": "Understand Group ICA for Multi-Subject Studies",
        "emoji": "👥",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 4,
        "url": "https://doi.org/10.1002/hbm.1048",
        "body_file": "03_understand_group_ica_for_multi_subject_studies.md",
    },
    {
        "task_name": "Learn Brain Networks",
        "emoji": "🧩",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 5,
        "url": "https://doi.org/10.1002/hbm.24580",
        "body_file": "04_learn_brain_networks.md",
    },
    {
        "task_name": "Read Key Lab Papers",
        "emoji": "📚",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 6,
        "url": "https://scholar.google.com/citations?user=e35VA6sAAAAJ&hl=en&sortby=pubdate",
        "body_file": "05_read_key_lab_papers.md",
    },
    {
        "task_name": "Learn Common Analysis Patterns in the Lab",
        "emoji": "🔬",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 7,
        "url": "https://trendscenter.org/software/gift/",
        "body_file": "06_learn_common_analysis_patterns.md",
    },
    {
        "task_name": "Interpret Functional Network Connectivity (FNC) Matrices",
        "emoji": "📊",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 8,
        "url": "https://doi.org/10.1093/cercor/bhs261",
        "body_file": "41_interpret_functional_connectivity.md",
    },

    # ----- Research Foundations (continued) — Preprocessing & QC -----
    {
        "task_name": "Understand Why fMRI Preprocessing Matters",
        "emoji": "🔧",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 9,
        "url": "https://andysbrainbook.readthedocs.io/en/latest/fMRI_Short_Course/fMRI_04_Preprocessing.html",
        "body_file": "07_understand_why_fmri_preprocessing_matters.md",
    },
    {
        "task_name": "Learn Quality Control for fMRI Data",
        "emoji": "✅",
        "category": "Research Foundations",
        "tier": "Theory",
        "order": 10,
        "url": "https://mriqc.readthedocs.io/en/latest/",
        "body_file": "10_learn_quality_control_for_fmri_data.md",
    },

    # ----- Statistical Analysis -----
    {
        "task_name": "Understand the General Linear Model (GLM)",
        "emoji": "📐",
        "category": "Statistical Analysis",
        "tier": "Theory",
        "order": 1,
        "url": "https://www.youtube.com/watch?v=gRhM04LfA2E",
        "body_file": "11_understand_the_general_linear_model.md",
    },
    {
        "task_name": "Learn Group Statistics (t-tests, ANOVA)",
        "emoji": "📈",
        "category": "Statistical Analysis",
        "tier": "Theory",
        "order": 2,
        "url": "https://www.youtube.com/watch?v=0Nc1NyBmUPU",
        "body_file": "12_learn_group_statistics.md",
    },
    {
        "task_name": "Understand Statistics for Neuroimaging",
        "emoji": "⚠️",
        "category": "Statistical Analysis",
        "tier": "Theory",
        "order": 3,
        "url": "https://doi.org/10.1073/pnas.1602413113",
        "body_file": "39_understand_statistics_for_neuroimaging.md",
    },

    # ----- Neuroimaging Software Ecosystem -----
    {
        "task_name": "Survey the Neuroimaging Software Landscape",
        "emoji": "🗺️",
        "category": "Neuroimaging Software",
        "tier": "Theory",
        "order": 1,
        "url": "https://andysbrainbook.readthedocs.io/en/latest/",
        "body_file": "13_survey_neuroimaging_software_landscape.md",
    },

    # ----- Writing & Publishing -----
    {
        "task_name": "Learn Scientific Writing Basics",
        "emoji": "✍️",
        "category": "Writing & Publishing",
        "tier": "Theory",
        "order": 1,
        "url": "https://www.youtube.com/watch?v=UY7sVKJPTMA",
        "body_file": "14_learn_scientific_writing_basics.md",
    },
    {
        "task_name": "Practice Reproducibility and Open Science",
        "emoji": "🔬",
        "category": "Writing & Publishing",
        "tier": "Theory",
        "order": 2,
        "url": "https://osf.io/",
        "body_file": "43_reproducibility_and_open_science.md",
    },

    # ======================================================================
    # TIER: Hands-On  (after theory)
    # ======================================================================

    # ----- Computing Environment (3 grouped evidence-based tasks) -----
    {
        "task_name": "Cluster Access & Connectivity",
        "emoji": "🔑",
        "category": "Computing Environment",
        "tier": "Hands-On",
        "order": 2,
        "url": "https://trendscenter.github.io/wiki/docs/Getting_Started.html",
        "body_file": "46_cluster_access_and_connectivity.md",
    },
    {
        "task_name": "Storage & File Management",
        "emoji": "📂",
        "category": "Computing Environment",
        "tier": "Hands-On",
        "order": 3,
        "url": "https://trendscenter.github.io/wiki/docs/Storage_guide.html",
        "body_file": "47_storage_and_file_management.md",
    },
    {
        "task_name": "SLURM Job Submission",
        "emoji": "📜",
        "category": "Computing Environment",
        "tier": "Hands-On",
        "order": 4,
        "url": "https://trendscenter.github.io/wiki/docs/SLURM_overview.html",
        "body_file": "48_slurm_job_submission.md",
    },
    {
        "task_name": "MATLAB Fundamentals",
        "emoji": "📐",
        "category": "Computing Environment",
        "tier": "Hands-On",
        "order": 5,
        "url": "https://matlabacademy.mathworks.com/",
        "body_file": "../tools/03_matlab.md",
    },

    # ----- Analysis Methods (ICA) -----
    {
        "task_name": "Install & Launch GIFT Toolbox",
        "emoji": "🧰",
        "category": "Analysis Methods",
        "tier": "Hands-On",
        "order": 1,
        "url": "https://trendscenter.org/software/gift/",
        "body_file": "30_install_and_launch_gift_toolbox.md",
    },
    {
        "task_name": "Run Your First Group ICA Analysis",
        "emoji": "🧪",
        "category": "Analysis Methods",
        "tier": "Hands-On",
        "order": 2,
        "url": "https://trendscenter.org/software/gift/",
        "body_file": "31_run_your_first_group_ica_analysis.md",
    },
    {
        "task_name": "Visualize & Sort ICA Components",
        "emoji": "👁️",
        "category": "Analysis Methods",
        "tier": "Hands-On",
        "order": 3,
        "url": "https://trendscenter.org/software/gift/",
        "body_file": "32_visualize_and_sort_ica_components.md",
    },
    {
        "task_name": "Debug and Troubleshoot ICA Analyses",
        "emoji": "🔍",
        "category": "Analysis Methods",
        "tier": "Hands-On",
        "order": 5,
        "url": "https://trendscenter.org/software/gift/",
        "body_file": "42_debug_and_troubleshoot_ica.md",
    },
    {
        "task_name": "Run Single-Subject Neuromark ICA on Cluster",
        "emoji": "🏃",
        "category": "Analysis Methods",
        "tier": "Hands-On",
        "order": 6,
        "url": "https://github.com/trendscenter/ClusterWorkshop",
        "body_file": "33_run_single_subject_neuromark_ica.md",
    },
    {
        "task_name": "Run Multi-Subject ICA with Array Jobs",
        "emoji": "👥",
        "category": "Analysis Methods",
        "tier": "Hands-On",
        "order": 7,
        "url": "https://github.com/trendscenter/ClusterWorkshop",
        "body_file": "34_run_multi_subject_ica_with_array_jobs.md",
    },
]

def main(delete_first=False):
    # Optionally delete all existing beginner tasks
    existing = query_data_source(TECHNICAL_DATA_SOURCE_ID)
    if delete_first and existing:
        print(f"Archiving {len(existing)} existing tasks...")
        for name, page_id in existing.items():
            print(f"  🗑️  {name}")
            archive_page(page_id)
        print()
        existing = {}  # All deleted, none to skip

    # Deduplicate: skip tasks that already exist
    tasks_to_create = [t for t in TASKS if t["task_name"] not in existing]
    skipped = len(TASKS) - len(tasks_to_create)
    if skipped:
        print(f"Skipping {skipped} tasks that already exist.\n")

    print(f"Creating {len(tasks_to_create)} beginner tasks...\n")

    for i, task in enumerate(tasks_to_create, 1):
        print(f"  [{i}/{len(tasks_to_create)}] {task['emoji']} {task['task_name']}")
        page_id = create_page(
            TECHNICAL_DATA_SOURCE_ID,
            task["task_name"],
            emoji=task["emoji"],
            url=task.get("url"),
            category=task.get("category"),
            tier=task.get("tier"),
            order=task.get("order"),
        )
        if page_id:
            # Load body from file if specified, otherwise use inline body
            body = None
            if task.get("body_file"):
                body_path = os.path.join(CONTENT_DIR, task["body_file"])
                if os.path.exists(body_path):
                    with open(body_path, "r", encoding="utf-8") as f:
                        body = f.read()
                else:
                    print(f"    ⚠ Body file not found: {task['body_file']}")
            elif task.get("body"):
                body = task["body"]
            if body:
                append_body_content(page_id, body)

    print("\nDone!")

if __name__ == "__main__":
    main()
