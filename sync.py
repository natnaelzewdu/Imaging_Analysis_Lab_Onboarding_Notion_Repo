"""
Sync onboarding content to Notion.

Each content/<tab>/ directory maps to one Notion data source (tab).
Tab configuration lives in content/<tab>/_tab.yaml — rename a folder freely,
no code changes needed.
Task metadata lives in YAML frontmatter at the top of each .md file.
Files without a 'task_name' frontmatter key are ignored.

LOCAL IS ALWAYS THE SOURCE OF TRUTH.
Running sync.py pushes local changes to Notion.
To pull Notion changes back to local files, use pull_notion.py.

Usage:
    python sync.py                              # Sync all tabs and pages
    python sync.py --tab <folder>               # Sync one tab or page
    python sync.py --category <name>            # Sync all tasks in a category
    python sync.py --task <filename.md>         # Sync one specific task file
    python sync.py --dry-run                    # Preview without writing to Notion
    python sync.py --status                     # Show local task inventory

    python pull_notion.py                       # Pull Notion content to local files
    python pull_notion.py --tab <folder>        # Pull one tab

Frontmatter keys (all optional except task_name):
    task_name  : (required) Exact title shown in Notion
    emoji      : Page icon  (default: 📌)
    tier       : Theory | Hands-On
    order      : Integer — controls sort order within a category
    url        : Reference link shown in Notion

Category is derived from the parent subfolder name, not from frontmatter.
"""

import argparse
import hashlib
import json
import os
import sys

# Ensure emoji and Unicode output works on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf-8-sig"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import yaml  # PyYAML

from notion_api import (
    append_body_content,
    archive_page,
    clear_page_blocks,
    create_page,
    ensure_database_properties,
    query_data_source,
)

CONTENT_ROOT = os.path.join(os.path.dirname(__file__), "content")
CACHE_FILE = os.path.join(os.path.dirname(__file__), ".sync_cache.json")


# ---------------------------------------------------------------------------
# Content hash cache — skip tasks whose body hasn't changed since last sync
# ---------------------------------------------------------------------------

def _load_cache() -> dict[str, str]:
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_cache(cache: dict[str, str]) -> None:
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def _body_hash(body: str) -> str:
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


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
# Plain-page discovery — reads _page.yaml from each content subfolder
# ---------------------------------------------------------------------------

def discover_pages() -> dict[str, dict]:
    """
    Scan content/ for subdirectories containing _page.yaml. These are plain
    Notion pages (not databases) whose full content is managed as a single
    .md file.

    _page.yaml format:
        label: "Welcome"
        notion_env_var: WELCOME_PAGE_ID
    """
    import importlib
    config_mod = importlib.import_module("config")

    pages: dict[str, dict] = {}
    if not os.path.isdir(CONTENT_ROOT):
        return pages

    for entry in sorted(os.listdir(CONTENT_ROOT)):
        page_dir = os.path.join(CONTENT_ROOT, entry)
        config_file = os.path.join(page_dir, "_page.yaml")
        if not os.path.isdir(page_dir) or not os.path.isfile(config_file):
            continue
        with open(config_file, encoding="utf-8") as fh:
            cfg = yaml.safe_load(fh) or {}
        env_var = cfg.get("notion_env_var")
        if not env_var:
            print(f"  Warning: {config_file} missing 'notion_env_var' key - skipping.")
            continue
        page_id = getattr(config_mod, env_var, None) or os.environ.get(env_var)
        if not page_id:
            print(f"  Warning: env var '{env_var}' is not set - skipping {entry}.")
            continue
        pages[entry] = {
            "page_id": page_id,
            "label": cfg.get("label", entry),
        }
    return pages


# ---------------------------------------------------------------------------
# Plain-page sync
# ---------------------------------------------------------------------------

def sync_page(
    folder_key: str,
    page_id: str,
    label: str,
    dry_run: bool = False,
) -> None:
    """
    Replace the full content of a plain Notion page from a local .md file.
    Unlike database tabs, this always does a full wipe + rewrite because there
    are no named rows to reconcile against.
    """
    print(f"\n{'=' * 60}")
    print(f"  {label}  (plain page)")
    print(f"{'=' * 60}")

    folder = os.path.join(CONTENT_ROOT, folder_key)
    md_files = sorted(f for f in os.listdir(folder) if f.endswith(".md"))

    if not md_files:
        print("  No .md files found.")
        return

    # Concatenate all .md files in the folder, stripping frontmatter if present
    body_parts = []
    for fname in md_files:
        with open(os.path.join(folder, fname), encoding="utf-8") as fh:
            raw = fh.read()
        if raw.startswith("---"):
            parts = raw.split("---", 2)
            raw = parts[2].lstrip("\n") if len(parts) >= 3 else raw
        body_parts.append(raw.strip())
    body = "\n\n".join(body_parts)

    if dry_run:
        print(f"  [DRY RUN] Would replace page content ({len(body)} chars from {len(md_files)} file(s)).")
        return

    print(f"  Clearing existing page content...")
    clear_page_blocks(page_id)
    print(f"  Pushing new content ({len(body)} chars)...")
    append_body_content(page_id, body)
    print(f"\n  Done.")




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
    sorted by order.

    Category is derived from the **parent subfolder name** — not the frontmatter
    key.  This means renaming a category folder automatically updates the Notion
    category on the next sync; no file edits are needed.

    Files sitting directly at the tab root (no subfolder) fall back to the
    'category' frontmatter key if present.
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

            # Derive category from parent folder name (overrides frontmatter)
            rel = os.path.relpath(root, tab_dir)
            if rel != ".":
                meta["category"] = rel  # folder name wins

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
        # Full wipe then recreate everything (also resets Status on all tasks)
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
            existing = {k: v for k, v in existing.items() if k not in orphans}

    if not tasks:
        print("  No publishable tasks found (files need YAML frontmatter with task_name).")
        return

    cache = _load_cache()
    cache_updated = False

    to_create = [t for t in tasks if t["task_name"] not in existing]
    to_update = [
        t for t in tasks
        if t["task_name"] in existing
        and _body_hash(t.get("_body", "")) != cache.get(t["task_name"])
    ]
    unchanged = len(tasks) - len(to_create) - len(to_update)

    # Update body content for tasks whose content has changed
    if to_update:
        print(f"  Updating body content for {len(to_update)} changed task(s)...\n")
        for task in to_update:
            name = task["task_name"]
            page_id = existing[name]
            print(f"    ✏  {name}")
            clear_page_blocks(page_id)
            if task.get("_body", "").strip():
                append_body_content(page_id, task["_body"])
            cache[name] = _body_hash(task.get("_body", ""))
            cache_updated = True
    elif unchanged:
        print(f"  {unchanged} task(s) unchanged — skipped.")

    if not to_create:
        if cache_updated:
            _save_cache(cache)
        print(f"\n  ✓ Done ({len(to_update)} updated, 0 created).")
        return

    print(f"\n  Creating {len(to_create)} new task(s)...\n")
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
            cache[name] = _body_hash(task.get("_body", ""))
            cache_updated = True

    if cache_updated:
        _save_cache(cache)
    print(f"\n  ✓ Done ({len(to_update)} updated, {len(to_create)} created).")


# ---------------------------------------------------------------------------
# Targeted sync helpers
# ---------------------------------------------------------------------------

def find_task_file(filename: str) -> str | None:
    """Search all content/ subdirectories for a .md file by filename."""
    for root, _dirs, files in os.walk(CONTENT_ROOT):
        if filename in files:
            return os.path.join(root, filename)
    return None


def sync_single_task(filepath: str, dry_run: bool = False) -> None:
    """Sync one specific .md file to its Notion page."""
    meta, body = parse_md(filepath)
    if not meta or not meta.get("task_name"):
        print(f"  No task_name frontmatter found in {filepath}")
        return

    # Determine which tab this file belongs to
    rel = os.path.relpath(filepath, CONTENT_ROOT)
    tab_key = rel.split(os.sep)[0]

    # Derive category from parent folder
    parent = os.path.basename(os.path.dirname(filepath))
    tab_dir = os.path.join(CONTENT_ROOT, tab_key)
    if os.path.dirname(filepath) != tab_dir:
        meta["category"] = parent

    tabs = discover_tabs()
    if tab_key not in tabs:
        print(f"  Tab '{tab_key}' not found in _tab.yaml discovery.")
        return

    data_source_id = tabs[tab_key]["data_source_id"]
    task_name = meta["task_name"]

    print(f"\n  Syncing task: {task_name}  [{tab_key}]")

    if dry_run:
        print(f"  [DRY RUN] Would update '{task_name}' in {tab_key}.")
        return

    ensure_database_properties(data_source_id)
    existing = query_data_source(data_source_id)

    if task_name in existing:
        page_id = existing[task_name]
        print(f"  Updating body content...")
        clear_page_blocks(page_id)
        if body.strip():
            append_body_content(page_id, body)
    else:
        print(f"  Creating new task...")
        page_id = create_page(
            data_source_id, task_name,
            emoji=meta.get("emoji", "📌"),
            url=meta.get("url"),
            category=meta.get("category"),
            tier=meta.get("tier"),
            order=meta.get("order"),
        )
        if page_id and body.strip():
            append_body_content(page_id, body)

    print(f"  ✓ Done.")


def sync_category(category_name: str, dry_run: bool = False) -> None:
    """Sync all tasks belonging to a category subfolder across all tabs."""
    tabs = discover_tabs()
    matched: list[tuple[str, str, dict]] = []  # (tab_key, filepath, meta)

    for tab_key in tabs:
        cat_dir = os.path.join(CONTENT_ROOT, tab_key, category_name)
        if not os.path.isdir(cat_dir):
            continue
        for fname in sorted(os.listdir(cat_dir)):
            if not fname.endswith(".md"):
                continue
            fpath = os.path.join(cat_dir, fname)
            meta, _ = parse_md(fpath)
            if meta and meta.get("task_name"):
                matched.append((tab_key, fpath, meta))

    if not matched:
        print(f"  No tasks found in category '{category_name}'.")
        return

    print(f"\n  Syncing category '{category_name}' ({len(matched)} task(s))...")

    if dry_run:
        for tab_key, fpath, meta in matched:
            print(f"    [DRY RUN] {meta['task_name']}  [{tab_key}]")
        return

    # Group by tab to minimise API calls
    from collections import defaultdict
    by_tab: dict[str, list] = defaultdict(list)
    for tab_key, fpath, meta in matched:
        by_tab[tab_key].append((fpath, meta))

    for tab_key, items in by_tab.items():
        data_source_id = tabs[tab_key]["data_source_id"]
        ensure_database_properties(data_source_id)
        existing = query_data_source(data_source_id)
        for fpath, meta in items:
            task_name = meta["task_name"]
            meta["category"] = category_name
            _, body = parse_md(fpath)
            if task_name in existing:
                page_id = existing[task_name]
                print(f"    ✏  {task_name}")
                clear_page_blocks(page_id)
                if body.strip():
                    append_body_content(page_id, body)
            else:
                print(f"    ➕  {task_name}")
                page_id = create_page(
                    data_source_id, task_name,
                    emoji=meta.get("emoji", "📌"),
                    url=meta.get("url"),
                    category=category_name,
                    tier=meta.get("tier"),
                    order=meta.get("order"),
                )
                if page_id and body.strip():
                    append_body_content(page_id, body)

    print(f"  ✓ Done.")


# ---------------------------------------------------------------------------
# Status report
# ---------------------------------------------------------------------------

def show_status() -> None:
    tabs = discover_tabs()
    pages = discover_pages()
    print("\nLocal inventory")
    print("=" * 60)
    total = 0
    for tab_key, info in tabs.items():
        tasks = load_tab_tasks(tab_key)
        total += len(tasks)
        print(f"\n  {info['label']}  ({len(tasks)} tasks)  [{tab_key}/]")
        for t in tasks:
            cat = t.get("category", "-")
            order = t.get("order", "-")
            print(f"    {t.get('emoji', '📌')}  #{order:>2}  [{cat}]  {t['task_name']}")
    if pages:
        print(f"\n  Plain pages:")
        for folder_key, info in pages.items():
            folder = os.path.join(CONTENT_ROOT, folder_key)
            md_files = [f for f in os.listdir(folder) if f.endswith(".md")]
            print(f"    {info['label']}  ({len(md_files)} file(s))  [{folder_key}/]")
    print(f"\nTotal: {total} tasks across {len(tabs)} tabs + {len(pages)} plain page(s)")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Push local .md content to Notion. Local is always the source of truth.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sync.py                                     # sync everything
  python sync.py --tab technical_onboarding          # sync one tab
  python sync.py --tab welcome                       # sync a Feed page (Welcome)
  python sync.py --category "Research Foundations"   # sync one category across all tabs
  python sync.py --task understand_what_fmri_measures.md  # sync one task file
  python sync.py --dry-run                           # preview without touching Notion
  python sync.py --status                            # show local inventory

  python pull_notion.py                              # pull Notion content to local files
  python pull_notion.py --tab technical_onboarding   # pull one tab
        """,
    )
    parser.add_argument("--tab", metavar="FOLDER",
                        help="Sync one tab or Feed page by folder name.")
    parser.add_argument("--task", metavar="FILE",
                        help="Sync one task by filename (e.g. read_lab_handbook.md).")
    parser.add_argument("--category", metavar="NAME",
                        help="Sync all tasks in a category subfolder.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Preview without writing to Notion.")
    parser.add_argument("--status", action="store_true",
                        help="Show local inventory and exit.")
    # --delete kept for power users but not advertised
    parser.add_argument("--delete", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    # --task
    if args.task:
        filepath = find_task_file(args.task)
        if not filepath:
            print(f"Task file '{args.task}' not found under content/.")
            sys.exit(1)
        sync_single_task(filepath, dry_run=args.dry_run)
        return

    # --category
    if args.category:
        sync_category(args.category, dry_run=args.dry_run)
        return

    tabs = discover_tabs()
    pages = discover_pages()
    all_folders = {**tabs, **pages}

    # --tab
    if args.tab:
        if args.tab not in all_folders:
            print(f"Unknown folder '{args.tab}'. Available: {', '.join(all_folders)}")
            sys.exit(1)
        if args.tab in pages:
            sync_page(args.tab, pages[args.tab]["page_id"], pages[args.tab]["label"],
                      dry_run=args.dry_run)
        else:
            sync_tab(args.tab, tabs[args.tab]["data_source_id"], tabs[args.tab]["label"],
                     delete_first=args.delete, dry_run=args.dry_run)
        if not args.dry_run:
            print("\nSync complete.")
        return

    # Default: sync everything
    for folder_key, info in pages.items():
        sync_page(folder_key, info["page_id"], info["label"], dry_run=args.dry_run)
    for tab_key, info in tabs.items():
        sync_tab(tab_key, info["data_source_id"], info["label"],
                 delete_first=args.delete, dry_run=args.dry_run)

    if not args.dry_run:
        print("\nSync complete.")


if __name__ == "__main__":
    main()
