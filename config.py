"""Centralized configuration loaded from environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
NOTION_DATABASE_ID = os.environ["NOTION_DATABASE_ID"]
HANDBOOK_DATA_SOURCE_ID = os.environ["HANDBOOK_DATA_SOURCE_ID"]
TECHNICAL_DATA_SOURCE_ID = os.environ["TECHNICAL_DATA_SOURCE_ID"]

NOTION_API_VERSION = "2026-03-11"
NOTION_BASE_URL = "https://api.notion.com/v1"
REQUEST_TIMEOUT = 120
RATE_LIMIT_DELAY = 0.5
