# Holiday Gifting Dashboard

> A reverse gift registry that transforms holiday stress into organized generosity.

Your gift-giving coordination system. It tracks what you're buying for others—not what you want them to buy for you. One dashboard. Complete clarity. Maximum peace of mind.

## The Problem

Gift-giving during the holidays creates unexpected cognitive load:

- What have you already bought for whom?
- Is your sister getting the same scarf from two family members?
- How much have you spent on each person?
- Which gifts are wrapped and ready?
- Where did you find that one perfect idea?

The Holiday Gifting Dashboard solves this with elegant simplicity.

## The Solution

A clean, mobile-responsive web application that lets you:

- **Track giftees** — Add the people you're shopping for with their relationships, budgets, and notes
- **Brainstorm gift ideas** — Store ranked ideas for each person with descriptions, links, and prices
- **Monitor progress** — Watch gifts move through four simple stages: considering → acquired → wrapped → given
- **Get AI suggestions** — Leverage Claude Haiku to brainstorm personalized gift ideas for 8 different relationship scenarios
- **Stay on budget** — See your total spending across all recipients at a glance
- **Never duplicate** — Centralized tracking prevents gift conflicts in families

## Key Features

### Intelligent Gift Tracking

Each gift idea flows through a natural lifecycle:

1. **Considering** — "I'm thinking about this..."
2. **Acquired** — "Got it! Checked off the list."
3. **Wrapped** — "Ready for delivery."
4. **Given** — "Mission accomplished!"

Move backwards if your plans change. No judgment. Flexibility is built in.

### AI-Powered Brainstorming

Stuck for ideas? The app integrates with Claude Haiku to generate personalized gift suggestions across eight relationship scenarios:

- Close Family
- Extended Family
- Significant Other
- Friends
- Colleagues
- Mentors
- Casual Relationships
- Budget-Conscious Gifting

Each suggestion considers the person, relationship context, and your constraints.

### Personal Dashboard

At a glance, see:

- All your giftees with progress indicators
- Budget tracking per person
- Total spending overview
- Quick-add buttons for new giftees and ideas
- Empty states with personality (because empty state design matters)

### Secure & Simple

- User authentication built in
- Your data stays in your database
- Works beautifully on mobile and desktop
- No account creation friction — just log in and start

## Quick Start

### Prerequisites

- Python 3.9+
- An Anthropic API key (for gift suggestions)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/holiday-gifting-dashboard.git
cd holiday-gifting-dashboard

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Anthropic API key and database path
```

### Running the App

```bash
# Initialize the database (first time only)
python init_db.py

# Start the Streamlit app
streamlit run app/main.py
```

The app will open at `http://localhost:8501`

### First Steps

1. Create your account
2. Add your first giftee
3. Start brainstorming gift ideas
4. Use AI suggestions when you need inspiration
5. Track your progress as you acquire and wrap gifts

## Technology Stack

**Frontend & Framework:**
- [Streamlit](https://streamlit.io/) — Python-based web framework for rapid UI development
- Clean, responsive design that works on all devices

**Backend & Database:**
- Python 3.9+
- [SQLAlchemy](https://www.sqlalchemy.org/) — ORM for database interactions
- SQLite for data persistence (easily portable to PostgreSQL)

**AI Integration:**
- [Anthropic Claude API](https://www.anthropic.com/) — Haiku model for gift brainstorming
- 8 specialized prompts for different relationship scenarios

**Authentication:**
- Bcrypt for secure password hashing
- Session-based user authentication

**Testing & Quality:**
- pytest for unit and integration testing
- pytest-cov for coverage reporting

## Project Structure

```
holiday-gifting-dashboard/
├── app/
│   ├── main.py                 # Main Streamlit application
│   ├── models.py               # SQLAlchemy data models
│   ├── database.py             # Database initialization & connection
│   ├── repository.py           # Data access layer
│   ├── config.py               # App configuration & constants
│   ├── services/
│   │   └── ai_service.py       # Claude integration & prompts
│   └── utils/
│       ├── helpers.py          # Utility functions
│       └── constants.py        # App constants & copy
├── init_db.py                  # Database initialization script
├── bootstrap.py                # Development utilities
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .streamlit/                 # Streamlit configuration
└── tests/                      # Test suite
```

## Development

### Running Tests

```bash
pytest tests/ -v --cov=app
```

### Environment Variables

See `.env.example` for required variables:

- `ANTHROPIC_API_KEY` — Your Claude API key
- `DATABASE_URL` — SQLite database path
- `APP_NAME` — Application display name
- `LOG_LEVEL` — Logging verbosity (DEBUG, INFO, WARNING)

### Design Philosophy

This project follows these principles:

1. **Velocity over perfection** — Ship working features quickly
2. **Delight in details** — Every interaction should feel intentional
3. **Progressive disclosure** — Start simple; reveal power features as needed
4. **Generous defaults** — Works beautifully with zero configuration

## Contributing

We welcome contributions! Here's how to get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Write or update tests
5. Commit with clear messages: `git commit -m "feat: add your feature"`
6. Push and open a pull request

See DEVELOPMENT.md for detailed guidelines.

## Roadmap

**Current Release (v1.0):**
- User authentication
- Giftee and gift idea CRUD
- 4-stage gift workflow
- AI-powered suggestions
- Budget tracking
- Mobile-responsive UI

**Future Enhancements:**
- Drag-to-reorder gift rankings
- Share giftee lists with partners
- Year-over-year history
- Gift idea URL import
- Advanced filtering and search

## License

MIT License

**Additional clause:** Merry Christmas 🎁

This project is open source and free to use. Built with care during the most wonderful time of the year.

## Built With

This project was developed with the assistance of:

- **Claude Code** — AI-powered development platform
- **Claude Haiku** — Efficient model for gift brainstorming
- **Anthropic's API** — Reliable, fast inference

Special thanks to the entire team who believed that gift-giving coordination deserves beautiful software.

## Questions? Ideas? Bug Reports?

Open an issue on GitHub. We're excited to hear from you.

---

**Your generosity coordination system awaits activation.** Start tracking, start organizing, and start gifting with confidence.
