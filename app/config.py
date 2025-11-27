"""
Configuration management for Holiday Gifting Dashboard.
Central location for all app configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATA_DIR}/holiday_gifts.db")

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key-change-this")

# Application
APP_NAME = os.getenv("APP_NAME", "Holiday Gifting Dashboard")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Status workflow
GIFT_STATUSES = ["considering", "acquired", "wrapped", "given"]
STATUS_COLORS = {
    "considering": "🔵",  # Gray
    "acquired": "🟢",     # Blue
    "wrapped": "🟣",      # Purple
    "given": "✅"         # Green
}

# UI Messages
EMPTY_STATES = {
    "no_giftees": "Your generosity awaits direction. Add someone to your list to begin.",
    "no_gifts": "The perfect gift is out there. Start brainstorming.",
    "all_acquired": "Acquisition complete. Your organizational excellence is noted.",
    "all_wrapped": "Peak preparedness achieved. You are ready."
}

# Session keys
SESSION_KEYS = {
    "user": "authenticated_user",
    "user_id": "user_id",
    "user_email": "user_email",
    "user_name": "user_name"
}
