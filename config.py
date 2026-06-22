"""Centralized configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
HANDBOOK_DATA_SOURCE_ID = os.environ["HANDBOOK_DATA_SOURCE_ID"]
TECHNICAL_DATA_SOURCE_ID = os.environ["TECHNICAL_DATA_SOURCE_ID"]
TOOLS_DATA_SOURCE_ID = os.environ["TOOLS_DATA_SOURCE_ID"]
FUNDING_DATA_SOURCE_ID = os.environ["FUNDING_DATA_SOURCE_ID"]
PROJECTS_DATA_SOURCE_ID = os.environ["PROJECTS_DATA_SOURCE_ID"]

# Plain page IDs (not databases) - optional, only needed if syncing those pages
WELCOME_PAGE_ID = os.environ.get("WELCOME_PAGE_ID", "")
LAB_LEADERSHIP_PAGE_ID = os.environ.get("LAB_LEADERSHIP_PAGE_ID", "")

NOTION_API_VERSION = "2026-03-11"
NOTION_BASE_URL = "https://api.notion.com/v1"
REQUEST_TIMEOUT = 120
RATE_LIMIT_DELAY = 0.35  # Notion allows ~3 req/s; 0.35s is safe
