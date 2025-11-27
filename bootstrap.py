#!/usr/bin/env python3
"""
Holiday Gifting Dashboard - Project Bootstrap Script
Investigator: Clive
Case: Rapid MVP Development
Status: Ready for Execution
"""

import os
import sys
from pathlib import Path

def create_project_structure():
    """Create the complete project directory structure."""

    base_path = Path.cwd()

    # Define directory structure
    directories = [
        "app",
        "app/pages",
        "app/components",
        "app/utils",
        "data",
        "tests",
        ".streamlit"
    ]

    # Create directories
    for directory in directories:
        path = base_path / directory
        path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

    # Create __init__.py files for Python packages
    init_files = [
        "app/__init__.py",
        "app/components/__init__.py",
        "app/utils/__init__.py"
    ]

    for init_file in init_files:
        path = base_path / init_file
        path.touch()
        print(f"✓ Created file: {init_file}")

def create_requirements_file():
    """Create requirements.txt with all dependencies."""

    requirements = """streamlit==1.29.0
streamlit-authenticator==0.3.1
sqlalchemy==2.0.23
pandas==2.1.4
python-dotenv==1.0.0
bcrypt==4.1.1
pytest==7.4.3
pytest-cov==4.1.0
"""

    with open("requirements.txt", "w") as f:
        f.write(requirements)
    print("✓ Created requirements.txt")

def create_env_example():
    """Create .env.example file."""

    env_content = """# Holiday Gifting Dashboard Configuration
# Copy this file to .env and update with your values

# Database
DATABASE_URL=sqlite:///data/holiday_gifts.db

# Secret key for session encryption (generate a random string)
SECRET_KEY=your-secret-key-here-change-this

# Application Settings
APP_NAME=Holiday Gifting Dashboard
DEBUG=false
"""

    with open(".env.example", "w") as f:
        f.write(env_content)
    print("✓ Created .env.example")

def create_gitignore():
    """Create .gitignore file."""

    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv
.env

# Database
*.db
*.sqlite
*.sqlite3
data/

# Streamlit
.streamlit/secrets.toml
.streamlit/credentials.toml

# IDE
.vscode/
.idea/
*.swp
*.swo
.DS_Store

# Testing
.pytest_cache/
.coverage
htmlcov/
*.cover

# Logs
*.log
"""

    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✓ Created .gitignore")

def create_streamlit_config():
    """Create Streamlit configuration."""

    config_content = """[theme]
primaryColor = "#7C3AED"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F3F4F6"
textColor = "#1F2937"

[server]
port = 8501
headless = true

[browser]
gatherUsageStats = false
"""

    with open(".streamlit/config.toml", "w") as f:
        f.write(config_content)
    print("✓ Created .streamlit/config.toml")

def create_config_py():
    """Create configuration management file."""

    config_content = '''"""
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
'''

    with open("app/config.py", "w") as f:
        f.write(config_content)
    print("✓ Created app/config.py")

def create_utils():
    """Create utility files."""

    constants_content = '''"""
Constants for Holiday Gifting Dashboard.
Investigator: Clive
Case File: Application Constants
"""

# Status progression
GIFT_STATUSES = ["considering", "acquired", "wrapped", "given"]

STATUS_COLORS = {
    "considering": {"bg": "#F3F4F6", "fg": "#6B7280", "emoji": "🤔"},
    "acquired": {"bg": "#DBEAFE", "fg": "#2563EB", "emoji": "✓"},
    "wrapped": {"bg": "#EDE9FE", "fg": "#7C3AED", "emoji": "🎁"},
    "given": {"bg": "#D1FAE5", "fg": "#059669", "emoji": "🎉"}
}

# Relationships (for dropdown)
RELATIONSHIPS = [
    "Partner",
    "Parent",
    "Sibling",
    "Child",
    "Friend",
    "Coworker",
    "Extended Family",
    "Other"
]

# Budget ranges (optional)
BUDGET_RANGES = [
    "Under $25",
    "$25-50",
    "$50-100",
    "$100-250",
    "$250-500",
    "Over $500",
    "No budget"
]
'''

    with open("app/utils/constants.py", "w") as f:
        f.write(constants_content)
    print("✓ Created app/utils/constants.py")

    helpers_content = '''"""
Helper functions for Holiday Gifting Dashboard.
Investigator: Clive
Case File: Utility Functions
"""

from typing import List, Dict, Any
import streamlit as st
from app.utils.constants import STATUS_COLORS, GIFT_STATUSES

def get_next_status(current_status: str) -> str:
    """Advance to next status in workflow."""
    try:
        current_index = GIFT_STATUSES.index(current_status)
        next_index = (current_index + 1) % len(GIFT_STATUSES)
        return GIFT_STATUSES[next_index]
    except ValueError:
        return GIFT_STATUSES[0]

def get_previous_status(current_status: str) -> str:
    """Return to previous status in workflow."""
    try:
        current_index = GIFT_STATUSES.index(current_status)
        prev_index = (current_index - 1) % len(GIFT_STATUSES)
        return GIFT_STATUSES[prev_index]
    except ValueError:
        return GIFT_STATUSES[0]

def calculate_progress(gifts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate gift progress statistics."""
    if not gifts:
        return {
            "total": 0,
            "acquired": 0,
            "wrapped": 0,
            "given": 0,
            "percentage": 0
        }

    total = len(gifts)
    acquired = sum(1 for g in gifts if g.get("status") in ["acquired", "wrapped", "given"])
    wrapped = sum(1 for g in gifts if g.get("status") in ["wrapped", "given"])
    given = sum(1 for g in gifts if g.get("status") == "given")

    return {
        "total": total,
        "acquired": acquired,
        "wrapped": wrapped,
        "given": given,
        "percentage": (acquired / total * 100) if total > 0 else 0
    }

def format_currency(amount: float) -> str:
    """Format amount as currency."""
    if amount is None:
        return ""
    return f"${amount:,.2f}"

def render_status_badge(status: str) -> str:
    """Render a status badge with appropriate styling."""
    colors = STATUS_COLORS.get(status, STATUS_COLORS["considering"])
    return f"{colors[\'emoji\']} {status.capitalize()}"
'''

    with open("app/utils/helpers.py", "w") as f:
        f.write(helpers_content)
    print("✓ Created app/utils/helpers.py")

def create_run_script():
    """Create a run.sh script for easy startup."""

    run_content = '''#!/bin/bash
# Holiday Gifting Dashboard - Quick Start Script
# Investigator: Clive
# Mission: Launch with maximum efficiency

echo "🎁 Holiday Gifting Dashboard - Starting Investigation..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po \'(?<=Python )[\d.]+\')
echo "✓ Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt --quiet

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your configuration"
fi

# Create data directory if it doesn't exist
mkdir -p data

# Run the application
echo "🚀 Launching Holiday Gifting Dashboard..."
echo "📍 Access at: http://localhost:8501"
echo "Press Ctrl+C to stop"
streamlit run app/main.py
'''

    with open("run.sh", "w") as f:
        f.write(run_content)

    # Make it executable
    os.chmod("run.sh", 0o755)
    print("✓ Created run.sh (executable)")

def main():
    """Execute the bootstrap sequence."""

    print("\n" + "="*60)
    print("🔍 Holiday Gifting Dashboard - Bootstrap Investigation")
    print("Detective: Clive | Status: Initializing Evidence")
    print("="*60 + "\n")

    print("Phase 1: Creating project structure...")
    create_project_structure()

    print("\nPhase 2: Setting up configuration...")
    create_requirements_file()
    create_env_example()
    create_gitignore()
    create_streamlit_config()
    create_config_py()

    print("\nPhase 3: Creating utilities...")
    create_utils()

    print("\nPhase 4: Creating launch script...")
    create_run_script()

    print("\n" + "="*60)
    print("✅ CASE CLOSED: Project structure ready!")
    print("="*60)
    print("\nNext steps:")
    print("1. Run: pip install -r requirements.txt")
    print("2. Copy .env.example to .env and update SECRET_KEY")
    print("3. Use the prompts in PROMPT_TEMPLATES.md to implement features")
    print("4. Run: ./run.sh to start the application")
    print("\nThe investigation continues. Happy coding, Detective! 🎁")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()