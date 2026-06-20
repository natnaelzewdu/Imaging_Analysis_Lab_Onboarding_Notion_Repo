"""
Unified CLI to push onboarding tasks to Notion.

Usage:
    python main.py --all              Push all task sets
    python main.py --handbook         Push handbook (Lab Culture & Conduct) tasks
    python main.py --beginner         Push beginner (Foundations & Setup) tasks
    python main.py --tools            Push tools & workflows tasks
    python main.py --funding          Push funding & fellowships tasks
    python main.py --projects         Push project tasks
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Push onboarding tasks to Notion.",
    )
    parser.add_argument("--all", action="store_true", help="Push all task sets")
    parser.add_argument("--handbook", action="store_true", help="Push handbook tasks (Lab Culture & Conduct)")
    parser.add_argument("--technical", action="store_true", help="Push technical tasks")
    parser.add_argument("--beginner", action="store_true", help="Push beginner tasks (Foundations & Setup)")
    parser.add_argument("--tools", action="store_true", help="Push tools & workflows tasks")
    parser.add_argument("--funding", action="store_true", help="Push funding & fellowships tasks")
    parser.add_argument("--projects", action="store_true", help="Push project tasks")
    parser.add_argument("--delete", action="store_true", help="Delete existing tasks before pushing")
    args = parser.parse_args()

    if not any([args.all, args.handbook, args.technical, args.beginner, args.tools, args.funding, args.projects]):
        parser.print_help()
        sys.exit(1)

    # Ensure Category/Tier/Order properties exist on the data sources
    from config import (
        HANDBOOK_DATA_SOURCE_ID, TECHNICAL_DATA_SOURCE_ID,
        TOOLS_DATA_SOURCE_ID, FUNDING_DATA_SOURCE_ID, PROJECTS_DATA_SOURCE_ID,
    )
    from notion_api import ensure_database_properties

    ds_ids = set()
    if args.all or args.handbook:
        ds_ids.add(HANDBOOK_DATA_SOURCE_ID)
    if args.all or args.technical or args.beginner:
        ds_ids.add(TECHNICAL_DATA_SOURCE_ID)
    if args.all or args.tools:
        ds_ids.add(TOOLS_DATA_SOURCE_ID)
    if args.all or args.funding:
        ds_ids.add(FUNDING_DATA_SOURCE_ID)
    if args.all or args.projects:
        ds_ids.add(PROJECTS_DATA_SOURCE_ID)

    print("Ensuring data source properties...")
    for ds_id in ds_ids:
        ensure_database_properties(ds_id)
    print()

    if args.all or args.handbook:
        print("=" * 60)
        print("LAB CULTURE & CONDUCT")
        print("=" * 60)
        from push_handbook_tasks import main as push_handbook
        push_handbook(delete_first=args.delete)
        print()

    if args.all or args.technical:
        print("=" * 60)
        print("TECHNICAL TASKS")
        print("=" * 60)
        from push_technical_tasks import main as push_technical
        push_technical()
        print()

    if args.all or args.beginner:
        print("=" * 60)
        print("FOUNDATIONS & SETUP")
        print("=" * 60)
        from push_beginner_tasks import main as push_beginner
        push_beginner(delete_first=args.delete)
        print()

    if args.all or args.tools:
        print("=" * 60)
        print("TOOLS & WORKFLOWS")
        print("=" * 60)
        from push_tools_tasks import main as push_tools
        push_tools(delete_first=args.delete)
        print()

    if args.all or args.funding:
        print("=" * 60)
        print("FUNDING & FELLOWSHIPS")
        print("=" * 60)
        from push_funding_tasks import main as push_funding
        push_funding(delete_first=args.delete)
        print()

    if args.all or args.projects:
        print("=" * 60)
        print("PROJECTS")
        print("=" * 60)
        from push_projects_tasks import main as push_projects
        push_projects(delete_first=args.delete)
        print()

    print("All done!")


if __name__ == "__main__":
    main()
