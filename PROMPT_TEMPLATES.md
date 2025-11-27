# Prompt Templates for Holiday Gifting Dashboard Implementation
## Ready-to-Execute Instructions for Each Development Phase

*Compiled by: Clive, Prompt Strategy Investigator*
*Purpose: Copy-paste ready prompts for immediate action*

---

## PROMPT 1: Database Implementation (Start Here)

```
Create a Python database layer for the Holiday Gifting Dashboard with SQLAlchemy.

Requirements:
1. Use SQLAlchemy ORM with SQLite for development
2. Three models: User, Giftee, GiftIdea
3. Status enum: considering, acquired, wrapped, given
4. All methods return dictionaries for Streamlit compatibility

Schema:
- User: id, email, name, password_hash, created_at
- Giftee: id, user_id, name, relationship, budget, notes, created_at
- GiftIdea: id, giftee_id, title, description, url, price, rank, status, created_at

Create app/database.py with:
- Model definitions
- DatabaseManager class
- Methods: create_user, authenticate_user, get_user_giftees, create_giftee, update_giftee, delete_giftee, create_gift_idea, update_gift_status, reorder_gift_ranks, get_giftee_with_ideas
- Proper session management
- Error handling

Include initialization function create_tables() and example usage.
```

---

## PROMPT 2: Streamlit Authentication Setup

```
Create an authentication system for a Streamlit Holiday Gifting Dashboard.

Requirements:
1. Use streamlit-authenticator library
2. Session state management for logged-in user
3. Registration flow for new users
4. Password hashing with bcrypt
5. Integration with SQLAlchemy User model

Create app/auth.py with:
- login_page() function showing login/register forms
- register_user() for new account creation
- authenticate() for login verification
- logout() for session cleanup
- require_auth() decorator for protected pages

The UI should be clean and match the "warm but efficient" tone from the spec.
Include helpful error messages and smooth transitions between login/register modes.
```

---

## PROMPT 3: Main Dashboard Implementation

```
Build the main dashboard for a Streamlit Holiday Gifting Dashboard.

This is the home page showing all giftees with their gift progress.

Requirements:
1. Grid layout of giftee cards showing:
   - Name and relationship
   - Progress bar (X of Y gifts acquired)
   - Budget if set
   - Click to navigate to detail

2. Quick-add giftee button with modal form

3. Summary metrics at top:
   - Total giftees
   - Total gifts planned
   - Overall progress
   - Total budget (if set)

4. Empty state when no giftees:
   "Your generosity awaits direction. Add someone to your list to begin."

5. Mobile responsive using Streamlit columns

Create app/pages/1_Dashboard.py implementing the full dashboard experience.
Use session state for smooth interactions and st.rerun() sparingly.
```

---

## PROMPT 4: Giftee Detail Page

```
Implement the giftee detail page for the Holiday Gifting Dashboard in Streamlit.

This page shows one giftee with all their gift ideas.

Requirements:
1. Header with giftee name, relationship, budget
2. Ranked list of gift ideas showing:
   - Rank number (draggable handle icon)
   - Title and description
   - Price and URL (if provided)
   - Status badge (clickable to change)
   - Edit/Delete buttons

3. Add gift idea form at bottom

4. Status progression: considering → acquired → wrapped → given
   - Click badge to advance
   - Right-click or hold to go back

5. Reorder functionality (number inputs for now, drag later)

6. Empty state: "The perfect gift is out there. Start brainstorming."

7. Success messages:
   - All acquired: "Acquisition complete. Your organizational excellence is noted."
   - All wrapped: "Peak preparedness achieved. You are ready."

Create app/pages/2_Giftee_Detail.py with full implementation.
```

---

## PROMPT 5: Component Library

```
Create reusable Streamlit components for the Holiday Gifting Dashboard.

Components needed:

1. status_badge(status, gift_id, callback):
   - Shows colored badge: gray (considering), blue (acquired), purple (wrapped), green (given)
   - Clickable to advance status
   - Returns new status when clicked

2. giftee_card(giftee, gifts):
   - Compact card with name, relationship
   - Progress bar showing X of Y acquired
   - Budget indicator if set
   - Clickable container

3. gift_idea_row(gift, on_update, on_delete):
   - Shows rank, title, price
   - Status badge
   - Edit/Delete actions
   - Clean layout

4. empty_state(message, action_label=None, action_callback=None):
   - Centered message with icon
   - Optional action button
   - Consistent styling

5. progress_ring(acquired, total):
   - Visual progress indicator
   - Shows percentage and count

Create app/components/ directory with each component in its own file.
Include demo usage in each file's __main__ block.
```

---

## PROMPT 6: Deployment Configuration

```
Setup deployment configuration for the Holiday Gifting Dashboard Streamlit app.

Requirements:
1. Support both Streamlit Cloud and Docker deployment
2. Environment variable management
3. Database initialization on first run
4. Proper secrets handling

Create these files:

1. requirements.txt with all dependencies
2. .env.example with required variables
3. config.py for centralized configuration
4. Dockerfile for containerized deployment
5. .streamlit/config.toml for Streamlit settings
6. deploy.sh script for one-command deployment

Include:
- Database auto-creation if not exists
- Migration support for schema changes
- Health check endpoint
- Proper logging configuration
- CORS and security headers

Ensure the app can run with just:
pip install -r requirements.txt
streamlit run app/main.py
```

---

## PROMPT 7: Testing Suite

```
Create a comprehensive test suite for the Holiday Gifting Dashboard.

Test coverage needed:
1. Database operations (CRUD for all models)
2. Authentication flow
3. Status progression logic
4. Gift ranking/reordering
5. Budget calculations
6. Empty states
7. Error handling

Create tests/ directory with:
- test_database.py: Model and manager tests
- test_auth.py: Login/register/session tests
- test_workflows.py: End-to-end user journeys
- test_components.py: UI component behavior
- fixtures.py: Sample data generation

Use pytest with good fixtures for database setup/teardown.
Include performance tests for operations that should be < 2 seconds.
Mock external dependencies appropriately.

Run with: pytest tests/ -v --cov=app
```

---

## PROMPT 8: Quick Start Documentation

```
Write user-facing documentation for the Holiday Gifting Dashboard.

Create an updated README.md that includes:

1. What This Is (2-3 sentences)
2. Quick Start (3 steps max)
3. Features list with screenshots
4. Installation instructions for:
   - Local development
   - Streamlit Cloud
   - Docker
   - Railway/Render

5. Usage Guide:
   - Adding your first giftee
   - Managing gift ideas
   - Tracking progress
   - Understanding statuses

6. FAQ section addressing:
   - Can multiple people use this?
   - How is data stored?
   - Is it mobile friendly?
   - Can I export my data?

7. Contributing guidelines
8. License (MIT)

Keep the tone warm and helpful. Include emoji sparingly (only in section headers).
Make it scannable with good formatting.
```

---

## PROMPT 9: Migration to Next.js (Future)

```
Create a migration plan from Streamlit to Next.js for v0.2 of the Holiday Gifting Dashboard.

Analyze the current Streamlit implementation and design a Next.js architecture that:

1. Preserves all existing functionality
2. Adds drag-to-reorder for gift rankings
3. Implements optimistic UI updates
4. Adds smooth animations and transitions
5. Improves mobile experience

Provide:
1. File structure for Next.js app
2. Component hierarchy diagram
3. API route specifications
4. State management strategy
5. Database migration approach
6. Deployment configuration
7. Step-by-step migration plan
8. Risk assessment

Keep the same data model but allow for future enhancements.
Maintain the "warm but efficient" tone in the UI.
```

---

## PROMPT 10: Performance Optimization

```
Optimize the Holiday Gifting Dashboard for production use.

Current stack: Streamlit + SQLAlchemy + SQLite

Optimization goals:
- Page load < 2 seconds
- Status updates < 500ms perceived
- Support 100 concurrent users
- Mobile performance parity

Implement:
1. Database query optimization
2. Caching strategy (Redis or in-memory)
3. Image/asset optimization
4. Lazy loading for gift lists
5. Connection pooling
6. Session state optimization
7. CDN setup for static assets
8. Monitoring and alerting

Provide specific code changes and configuration updates.
Include before/after performance metrics.
Document trade-offs made.
```

---

## EMERGENCY PROMPT: Debug Assistant

```
I'm building a Holiday Gifting Dashboard with Streamlit and encountering [DESCRIBE ISSUE].

Context:
- Streamlit app for tracking gifts you're giving to others
- SQLAlchemy with SQLite database
- Three models: User, Giftee, GiftIdea
- Status flow: considering → acquired → wrapped → given

Current error: [PASTE ERROR]

Relevant code: [PASTE CODE SNIPPET]

Expected behavior: [WHAT SHOULD HAPPEN]

What I've tried: [LIST ATTEMPTS]

Please help me:
1. Understand why this is happening
2. Fix the immediate issue
3. Prevent similar issues
4. Improve the implementation if needed

Keep solutions simple and aligned with "velocity over perfection" principle.
```

---

## MASTER PROMPT: Full Implementation in One Go

```
Build a complete Holiday Gifting Dashboard MVP using Python and Streamlit.

This is a "reverse gift registry" - instead of listing what you want, you track what you're getting for others.

Core Features:
1. User authentication (login/register)
2. Manage multiple giftees (people you're shopping for)
3. Track gift ideas per giftee with ranking
4. Status progression: considering → acquired → wrapped → given
5. Dashboard showing all giftees with progress
6. Mobile responsive design

Technical Requirements:
- Streamlit for UI
- SQLAlchemy with SQLite
- streamlit-authenticator for auth
- Session state for smooth UX
- Clean, organized code structure

Data Model:
- User (id, email, name, password_hash, created_at)
- Giftee (id, user_id, name, relationship, budget, notes, created_at)
- GiftIdea (id, giftee_id, title, description, url, price, rank, status, created_at)

UI Personality:
- Warm but efficient
- Quietly confident
- Empty states with personality
- Focus on progress and celebration

Create a complete, working application with:
1. app/database.py - Models and database manager
2. app/auth.py - Authentication system
3. app/main.py - Main application entry
4. app/pages/ - Dashboard and detail pages
5. requirements.txt - All dependencies
6. README.md - User documentation

The app should be immediately runnable with:
pip install -r requirements.txt
streamlit run app/main.py

Prioritize working code over perfect code. Ship it.
```

---

*These prompts are sequenced for optimal development flow. Start with Prompt 1 and progress linearly for best results.*

*Remember: The case demands swift action. Execute with precision.*