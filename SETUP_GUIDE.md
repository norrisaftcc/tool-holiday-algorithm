# Setup Guide - Holiday Gifting Dashboard

## Overview

This guide walks through the project setup that has been completed, and how to get started developing.

## Completed Setup

The following has already been done for you:

### 1. Project Structure
- **app/** - Main application code
  - `main.py` - Streamlit application entry point
  - `models.py` - SQLAlchemy ORM models (User, Giftee, GiftIdea)
  - `database.py` - Database connection and initialization
  - `repository.py` - Data access layer with query methods
  - `config.py` - Configuration management
  - **components/** - Reusable Streamlit components (ready for expansion)
  - **pages/** - Multi-page app structure (ready for expansion)
  - **utils/** - Helper functions and constants
    - `constants.py` - Status values, relationships, budget ranges
    - `helpers.py` - Utility functions for progress tracking, formatting

### 2. Database
- SQLite database created at `data/holiday_gifts.db`
- Three core tables:
  - `users` - User accounts with bcrypt password hashing
  - `giftees` - People you're shopping for
  - `gift_ideas` - Individual gift ideas with status tracking

### 3. Configuration
- `.env` - Local development environment (created)
- `.env.example` - Template with all available configuration options
- `.streamlit/config.toml` - Streamlit UI configuration (purple theme)
- `requirements.txt` - Python dependencies

### 4. Virtual Environment
- Python virtual environment set up at `venv/`
- All dependencies installed

## Quick Start

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Initialize Database (if needed)
```bash
python3 init_db.py
```

This creates sample data:
- Demo user: demo@example.com / demo123
- Sample giftees: Alice Johnson, Bob Smith
- Sample gift ideas with various statuses

### 3. Start the Application
```bash
streamlit run app/main.py
```

Or use the convenient launch script:
```bash
./run.sh
```

The app will be available at: http://localhost:8501

### 4. Log In
Use the demo credentials or register a new account:
- **Email:** demo@example.com
- **Password:** demo123

## Project Architecture

### Authentication & Sessions
- User registration with email and password
- Bcrypt password hashing for security
- Session-based authentication stored in Streamlit session state
- Users can only see their own giftees

### Data Access Pattern
The repository pattern is used for clean data access:
```
UI (Streamlit)
  ↓
Repository (UserRepository, GifteeRepository, GiftIdeaRepository)
  ↓
Models (SQLAlchemy ORM)
  ↓
Database (SQLite)
```

### Key Classes

**Models (app/models.py):**
- `User` - User accounts
- `Giftee` - People receiving gifts
- `GiftIdea` - Individual gift ideas

**Repository (app/repository.py):**
- `UserRepository` - User CRUD and authentication
- `GifteeRepository` - Giftee management
- `GiftIdeaRepository` - Gift idea management

**Configuration (app/config.py):**
- Database URL
- Status values and colors
- UI messages and empty states
- Session key names

## Core Features

### MVP (Currently Implemented)
- [x] User authentication (email/password signup and login)
- [x] Add/edit/delete giftees
- [x] Add/edit/delete gift ideas
- [x] Status tracking (considering → acquired → wrapped → given)
- [x] Progress overview
- [x] Budget tracking per giftee
- [x] Mobile-responsive design

### Development Structure
- Clean separation of concerns
- Repository pattern for data access
- Type hints with Pydantic models
- Environment-based configuration
- Ready for feature expansion

## File Reference

### Core Application Files
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/app/main.py` - Main Streamlit app
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/app/models.py` - Database models
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/app/database.py` - DB connection
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/app/repository.py` - Data access
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/app/config.py` - Configuration

### Configuration
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/.env` - Development secrets
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/.env.example` - Template
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/.streamlit/config.toml` - Streamlit config
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/requirements.txt` - Dependencies

### Database
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/data/holiday_gifts.db` - SQLite database
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/init_db.py` - DB initialization

### Utilities
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/app/utils/constants.py` - App constants
- `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/app/utils/helpers.py` - Helper functions

## Environment Variables

Key variables in `.env`:

```
DATABASE_URL=sqlite:///data/holiday_gifts.db  # Database connection
SECRET_KEY=dev-secret-key-change-before-production  # Session secret
APP_NAME=Holiday Gifting Dashboard  # App title
DEBUG=true  # Enable debug mode
```

For production deployment, update these in `.env`:
- `DEBUG=false`
- `SECRET_KEY` - Use a strong random string
- `DATABASE_URL` - Point to PostgreSQL for production

## Next Steps for Development

### To Add a New Feature:
1. Update data model in `app/models.py` if needed
2. Add repository methods in `app/repository.py`
3. Add UI in `app/main.py` or create a new page
4. Update constants/helpers if needed

### To Create a New Page:
1. Create file in `app/pages/`
2. Use Streamlit multi-page app structure
3. Import and use existing repositories

### To Extend Components:
Components directory is set up for reusable Streamlit components in `app/components/`

## Database Management

### Reset Database
```python
from app.database import reset_db
reset_db()  # WARNING: Destructive - deletes all data
```

### Check Tables
```python
from app.database import table_exists
table_exists("users")  # Returns True/False
```

## Dependencies

Core packages installed:
- **streamlit** - Web app framework
- **sqlalchemy** - ORM and database toolkit
- **bcrypt** - Password hashing
- **python-dotenv** - Environment variable management
- **pandas** - Data manipulation (available for future features)
- **pytest** - Testing framework

Full list in `/Users/norrisa/Documents/dev/github/tool-holiday-algorithm/requirements.txt`

## Documentation

Additional documentation available:
- `CLAUDE.md` - Project vision and design philosophy
- `IMPLEMENTATION_STRATEGY.md` - Implementation approach and roadmap
- `PROMPT_TEMPLATES.md` - AI assistant prompts for feature development

## Troubleshooting

### Database Issues
If database gets corrupted:
```bash
rm data/holiday_gifts.db
python3 init_db.py
```

### Virtual Environment Issues
Recreate virtual environment:
```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Streamlit Cache Issues
Clear Streamlit cache:
```bash
streamlit cache clear
```

## Git Workflow

Branch naming convention:
```
feature/add-gift-suggestions
fix/status-not-updating
chore/update-dependencies
```

Commit message format:
```
feat: add gift suggestion feature
fix: correct status update logic
docs: update README with setup guide
```

---

**Ready to develop! The foundation is solid, clean, and ready for rapid iteration.**
