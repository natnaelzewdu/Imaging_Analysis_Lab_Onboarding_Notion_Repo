"""
Sync onboarding content to Notion.

Each content/<tab>/ directory maps to one Notion data source (tab).
Tab configuration lives in content/<tab>/_tab.yaml — rename a folder freely,
no code changes needed.
Task metadata lives in YAML frontmatter at the top of each .md file.
Files without a 'task_name' frontmatter key are ignored.

Usage:
    python sync.py                          # Reconcile all tabs
    python sync.py --tab technical_onboarding  # Reconcile one tab
    python sync.py --delete                 # Full wipe + re-sync (use after editing body content)
    python sync.py --dry-run                # Preview without writing to Notion
    python sync.py --status                 # Show local task counts per tab

Frontmatter keys (all optional except task_name):
    task_name  : (required) Exact title shown in Notion
    emoji      : Page icon  (default: 📌)
    category   : Select property value — should match the subfolder name
    tier       : Select property value  (Theory | Hands-On)
    order      : Number property for sorting within a category
    url        : URL property
"""

import argparse
import os
import sys

# Ensure emoji and Unicode output works on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import yaml  # PyYAML

from notion_api import (
    append_body_content,
    archive_page,
    create_page,
    ensure_database_properties,
    query_data_source,
)

CONTENT_ROOT = os.path.join(os.path.dirname(__file__), "content")


# ---------------------------------------------------------------------------
# Dynamic tab discovery — reads _tab.yaml from each content subfolder
# ---------------------------------------------------------------------------

def discover_tabs() -> dict[str, dict]:
    """
    Scan content/ for subdirectories containing _tab.yaml and build the tab
    registry.  This means you can rename a tab folder without touching any
    Python code — just rename the directory.

    _tab.yaml format:
        label: "Human-readable tab name"
        notion_env_var: FUNDING_DATA_SOURCE_ID
    """
    import importlib
    config_mod = importlib.import_module("config")

    tabs: dict[str, dict] = {}
    if not os.path.isdir(CONTENT_ROOT):
        return tabs

    for entry in sorted(os.listdir(CONTENT_ROOT)):
        tab_dir = os.path.join(CONTENT_ROOT, entry)
        config_file = os.path.join(tab_dir, "_tab.yaml")
        if not os.path.isdir(tab_dir) or not os.path.isfile(config_file):
            continue
        with open(config_file, encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        env_var = cfg.get("notion_env_var")
        if not env_var:
            print(f"  ⚠  {config_file}: missing 'notion_env_var' key — skipping tab.")
            continue
        data_source_id = getattr(config_mod, env_var, None) or os.environ.get(env_var)
        if not data_source_id:
            print(f"  ⚠  {config_file}: env var '{env_var}' is not set — skipping tab.")
            continue
        tabs[entry] = {
            "data_source_id": data_source_id,
            "label": cfg.get("label", entry),
        }
    return tabs


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_md(filepath: str) -> tuple[dict | None, str]:
    """
    Parse YAML frontmatter + body from a Markdown file.

    Returns (frontmatter_dict, body_text).
    If the file has no '---' frontmatter block, returns (None, full_content).
    """
    with open(filepath, encoding="utf-8") as fh:
        raw = fh.read()

    if not raw.startswith("---"):
        return None, raw

    parts = raw.split("---", 2)
    if len(parts) < 3:
        return None, raw

    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        print(f"  ⚠ YAML error in {filepath}: {exc}")
        return None, raw

    body = parts[2].lstrip("\n")
    return meta, body


def load_tab_tasks(tab_key: str) -> list[dict]:
    """
    Load all publishable tasks from a tab directory (including category subfolders),
    sorted by order.  Any .md file anywhere under content/<tab>/ that has a
    'task_name' frontmatter key is included.
    """
    tab_dir = os.path.join(CONTENT_ROOT, tab_key)
    if not os.path.isdir(tab_dir):
        return []

    tasks = []
    for root, _dirs, files in os.walk(tab_dir):
        for fname in sorted(files):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(root, fname)
            meta, body = parse_md(fpath)
            if not meta or not meta.get("task_name"):
                continue
            tasks.append({**meta, "_body": body, "_file": os.path.relpath(fpath, tab_dir)})

    tasks.sort(key=lambda t: (t.get("order") or 999))
    return tasks


# ---------------------------------------------------------------------------
# Core sync logic
# ---------------------------------------------------------------------------

def sync_tab(
    tab_key: str,
    data_source_id: str,
    label: str,
    delete_first: bool = False,
    dry_run: bool = False,
) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {label}")
    print(f"{'=' * 60}")

    tasks = load_tab_tasks(tab_key)
    local_names = {t["task_name"] for t in tasks}

    if dry_run:
        print(f"  [DRY RUN] {len(tasks)} local task(s):\n")
        for t in tasks:
            cat = t.get("category", "—")
            tier = t.get("tier", "—")
            order = t.get("order", "—")
            print(f"    {t.get('emoji', '📌')}  [{cat} | {tier} | #{order}]  {t['task_name']}")
        return

    # Ensure required Notion properties exist
    ensure_database_properties(data_source_id)

    existing = query_data_source(data_source_id)

    if delete_first:
        # Full wipe then recreate everything
        if existing:
            print(f"  Archiving {len(existing)} existing page(s)...")
            for name, page_id in existing.items():
                print(f"    🗑  {name}")
                archive_page(page_id)
        existing = {}
    else:
        # Reconcile: archive Notion pages that no longer have a local file
        orphans = {name: pid for name, pid in existing.items() if name not in local_names}
        if orphans:
            print(f"  Archiving {len(orphans)} removed task(s)...")
            for name, page_id in orphans.items():
                print(f"    🗑  {name}")
                archive_page(page_id)
                del existing[name]  # type: ignore[attr-defined]
            existing = {k: v for k, v in existing.items() if k not in orphans}

    if not tasks:
        print("  No publishable tasks found (files need YAML frontmatter with task_name).")
        return

    to_create = [t for t in tasks if t["task_name"] not in existing]
    skipped = len(tasks) - len(to_create)
    if skipped:
        print(f"  Skipping {skipped} already-existing task(s).")

    if not to_create:
        print("  Nothing to do — all tasks already exist in Notion.")
        return

    print(f"  Creating {len(to_create)} task(s)...\n")
    for i, task in enumerate(to_create, 1):
        emoji = task.get("emoji", "📌")
        name = task["task_name"]
        print(f"  [{i}/{len(to_create)}] {emoji}  {name}")
        page_id = create_page(
            data_source_id,
            name,
            emoji=emoji,
            url=task.get("url"),
            category=task.get("category"),
            tier=task.get("tier"),
            order=task.get("order"),
        )
        if page_id and task.get("_body", "").strip():
            append_body_content(page_id, task["_body"])

    print(f"\n  ✓ Done ({len(to_create)} created).")


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------

def show_status() -> None:
    tabs = discover_tabs()
    print("\nLocal task inventory")
    print("=" * 60)
    total = 0
    for tab_key, info in tabs.items():
        tasks = load_tab_tasks(tab_key)
        total += len(tasks)
        print(f"\n  {info['label']}  ({len(tasks)} tasks)  [{tab_key}/]")
        for t in tasks:
            cat = t.get("category", "—")
            order = t.get("order", "—")
            print(f"    {t.get('emoji', '📌')}  #{order:>2}  [{cat}]  {t['task_name']}")
    print(f"\nTotal: {total} tasks across {len(tabs)} tabs")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync Notion onboarding content from local .md files.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sync.py                            # sync everything (safe, idempotent)
  python sync.py --tab technical_onboarding # sync one tab only
  python sync.py --delete                   # wipe + re-sync all tabs
  python sync.py --tab lab_intro --delete   # wipe + re-sync one tab
  python sync.py --dry-run                  # preview without touching Notion
  python sync.py --status                   # count local tasks per tab
        """,
    )
    parser.add_argument(
        "--tab",
        metavar="TAB",
        help="Only sync this tab folder name (e.g. technical_onboarding).",
    )
    parser.add_argument(
        "--delete",
        action="store_true",
        help="Archive all existing Notion pages in the target tab(s) before syncing.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without writing to Notion.",
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Show local task inventory and exit.",
    )
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    tabs = discover_tabs()

    if args.tab:
        if args.tab not in tabs:
            print(f"Unknown tab '{args.tab}'. Available tabs: {', '.join(tabs)}")
            sys.exit(1)
        tabs_to_sync = {args.tab: tabs[args.tab]}
    else:
        tabs_to_sync = tabs

    for tab_key, info in tabs_to_sync.items():
        sync_tab(
            tab_key,
            info["data_source_id"],
            info["label"],
            delete_first=args.delete,
            dry_run=args.dry_run,
        )

    if not args.dry_run:
        print("\nSync complete.")


if __name__ == "__main__":
    main()
