# Notion Onboarding — Imaging-Analysis Lab

Programmatically manages onboarding content in Notion for the **Imaging-Analysis Lab (TReNDS Center, GSU)**.

All task content lives in plain Markdown files. A single command syncs everything to Notion — no Python editing required to add, edit, or remove tasks.

---

## Table of Contents

- [How it works](#how-it-works)
- [Repository structure](#repository-structure)
- [Setup](#setup)
- [Everyday workflows](#everyday-workflows)
  - [Add a new task](#add-a-new-task)
  - [Edit an existing task](#edit-an-existing-task)
  - [Delete a task](#delete-a-task)
  - [Sync to Notion](#sync-to-notion)
  - [Pull content from Notion](#pull-content-from-notion)
- [Frontmatter reference](#frontmatter-reference)
- [For AI agents](#for-ai-agents)
- [Environment variables](#environment-variables)

---

## How it works

Each Notion tab corresponds to a folder under `content/`:

| Notion tab           | Local folder                        | Env var                    |
|----------------------|-------------------------------------|----------------------------|
| Lab Intro            | `content/lab_intro/`                | `HANDBOOK_DATA_SOURCE_ID`  |
| Technical Onboarding | `content/technical_onboarding/`     | `TECHNICAL_DATA_SOURCE_ID` |
| Tools & Workflows    | `content/tools/`                    | `TOOLS_DATA_SOURCE_ID`     |
| Funding & Fellowships| `content/funding/`                  | `FUNDING_DATA_SOURCE_ID`   |
| Projects             | `content/projects/`                 | `PROJECTS_DATA_SOURCE_ID`  |

Every `.md` file with a YAML frontmatter block (see below) is treated as one Notion task page. Files without frontmatter are ignored by the sync script.

---

## Repository structure

```
.env.example                   ← copy to .env and fill in your tokens
sync.py                        ← THE entry point — syncs .md files → Notion
pull_notion.py                 ← pull Notion content back to .md files
config.py                      ← loads env vars (do not edit)
notion_api.py                  ← Notion API helpers (do not edit)
requirements.txt

content/
  lab_intro/                   ← Lab Intro tab
  technical_onboarding/        ← Technical Onboarding tab
  tools/                       ← Tools & Workflows tab
  funding/                     ← Funding & Fellowships tab
  projects/                    ← Projects tab

data/                          ← Raw source files (Word docs, spreadsheets, photos)
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/<org>/notion-onboarding.git
cd notion-onboarding
```

### 2. Create a virtual environment

```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in each value:

```bash
cp .env.example .env
```

> **Important — Notion Personal Access Token:**
> `NOTION_TOKEN` must be a Notion **Internal Integration Token** with read/write
> access to each database listed in the env file.
>
> To create one: Notion → Settings → Integrations → Create new integration.
> Then share each database with the integration via the database's "Connect to"
> menu.

The `*_DATA_SOURCE_ID` values are the IDs of the Notion databases backing each
tab. Find them by opening the database in Notion and copying the UUID from the
URL: `notion.so/<workspace>/<**THIS-UUID**>?v=...`

---

## Everyday workflows

The **`.md` file is the source of truth**. Edit the file, run `sync.py`, and Notion reflects the change. The sync is a **reconcile by default** — it compares local files against Notion and:

- Creates pages that exist locally but not in Notion
- Archives pages that exist in Notion but no longer have a local file
- Skips pages that already exist with the same `task_name` (use `--delete` to force-update body content)

### Add a new task

1. Create a new `.md` file in the appropriate `content/<tab>/<category>/` folder.  
   Name it descriptively: `understand_bold_signal.md` — no number prefix needed.

2. Add YAML frontmatter at the top:

   ```markdown
   ---
   task_name: "Understand the BOLD Signal"
   emoji: "🧲"
   category: Research Foundations
   tier: Theory
   order: 13
   url: "https://example.com/resource"
   ---

   ## Why this matters
   Write the task body here in standard Markdown...
   ```

3. Run `python sync.py` (or `--tab <folder>`). The new page is created in Notion.

### Edit an existing task

**Body content changed** (the Markdown below the frontmatter):

Notion's API does not support in-place block updates — the page must be
archived and recreated. Run:

```bash
python sync.py --tab <folder> --delete
```

**Frontmatter only changed** (task name, emoji, category, tier, order, url):

Same as above — use `--delete` to wipe the old page and recreate it with the
updated metadata.

> **Tip:** `--delete` only affects the one tab you specify. Other tabs are untouched.

### Delete a task

1. Delete the `.md` file (or rename it without a `task_name` frontmatter key).
2. Run `python sync.py` — the sync automatically detects the removed file and
   archives the corresponding Notion page.

### Move a task to a different category

1. Move the `.md` file to `content/<tab>/<NewCategory>/` (create the folder if needed).
2. Update the `category` frontmatter key to match the new folder name.
3. Run `python sync.py --tab <folder> --delete` to re-publish with the new category.

### Rename a task

1. Update `task_name` in the frontmatter.
2. Run `python sync.py --tab <folder> --delete` — the old-named page is archived
   and the renamed page is created.

### Sync to Notion

```bash
# Reconcile all tabs (create new + archive removed — safe to run anytime)
python sync.py

# Reconcile one tab only
python sync.py --tab technical_onboarding

# Preview what would happen without touching Notion
python sync.py --dry-run

# Force full wipe + re-sync a tab (required after editing body content)
python sync.py --tab lab_intro --delete

# Check local task inventory
python sync.py --status
```

### Pull content from Notion

If someone edited task body content directly in Notion and you want to sync
those changes back to the local `.md` files:

```bash
python pull_notion.py                              # pull all tabs
python pull_notion.py --tab technical_onboarding  # pull one tab
python pull_notion.py --dry-run                    # preview only
```

> The pull script preserves each file's YAML frontmatter and replaces only the
> body section below it.

## Frontmatter reference

| Key         | Required | Description                                           |
|-------------|----------|-------------------------------------------------------|
| `task_name` | **Yes**  | Exact title shown in Notion                           |
| `emoji`     | No       | Page icon (default: `📌`)                             |
| `category`  | No       | Notion `Category` select property                     |
| `tier`      | No       | `Theory` or `Hands-On`                                |
| `order`     | No       | Integer — controls sort order within a category       |
| `url`       | No       | Reference link shown in Notion                        |

Files without a `task_name` key are silently skipped by `sync.py` and
`pull_notion.py`. This lets you keep notes or archived content in the same
folder without accidentally publishing them.

---

## For AI agents

This repo is structured to be easily operated by AI coding agents. Key facts:

- **Single entry point:** `python sync.py [options]` — no other scripts needed for CRUD.
- **Data lives in `.md` files:** All task content and metadata is in `content/<tab>/*.md`. Agents should read/write these files.
- **Frontmatter drives Notion:** Change the frontmatter to change how a task appears in Notion. Change the body to change the task's page content.
- **Idempotent by default:** Running `sync.py` without `--delete` never overwrites existing Notion pages.
- **Tab mapping:** see the table in [How it works](#how-it-works).
- **No Python editing needed** for ordinary CRUD — only `.md` files.

Suggested agent workflow for a content change:
1. Read the relevant `.md` file(s) in `content/<tab>/<category>/`.
2. Modify frontmatter and/or body as needed.
3. Run `python sync.py --dry-run` to verify the change looks correct.
4. Run `python sync.py --tab <tab>` for adds/deletes (auto-reconciles).
5. Run `python sync.py --tab <tab> --delete` if body content was edited.

---

## Environment variables

| Variable                  | Description                                          |
|---------------------------|------------------------------------------------------|
| `NOTION_TOKEN`            | **Notion Internal Integration Token** (secret)       |
| `NOTION_DATABASE_ID`      | Legacy — kept for backwards compatibility            |
| `HANDBOOK_DATA_SOURCE_ID` | Notion database ID for the Lab Intro tab             |
| `TECHNICAL_DATA_SOURCE_ID`| Notion database ID for the Technical Onboarding tab  |
| `TOOLS_DATA_SOURCE_ID`    | Notion database ID for the Tools & Workflows tab     |
| `FUNDING_DATA_SOURCE_ID`  | Notion database ID for the Funding & Fellowships tab |
| `PROJECTS_DATA_SOURCE_ID` | Notion database ID for the Projects tab              |

> Store these in a `.env` file at the repo root. The `.env` file is gitignored
> and must **never** be committed.
