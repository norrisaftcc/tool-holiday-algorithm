"""
Pytest Configuration and Shared Fixtures

EDUCATIONAL NOTE FOR STUDENTS:
================================
This file is special! The name "conftest.py" is recognized by pytest.
Any fixtures defined here are automatically available to ALL test files
in this directory and subdirectories.

Think of this as your "test utilities toolbox" - reusable setup code
that many tests need.

Key Concepts You'll Learn:
- What fixtures are and why they're useful
- Test isolation (each test gets a fresh database)
- Setup and teardown patterns
- Fixture scopes (function, session, module)
- Fixture composition (fixtures using other fixtures)

Author: Holiday Gifting Dashboard Team
Purpose: Educational test infrastructure for CS students
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, User, Giftee, GiftIdea
import bcrypt


# =============================================================================
# CORE FIXTURES - Database Setup
# =============================================================================

@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh in-memory database for EACH test function.

    LEARNING OBJECTIVE: Test Isolation
    ===================================
    Every test should be independent. If Test A creates a user named "Alice",
    Test B shouldn't see that user. This fixture ensures each test starts
    with a clean, empty database.

    Why "scope='function'"?
    -----------------------
    This means a NEW database is created for every single test function.
    Pros: Perfect isolation, tests can't affect each other
    Cons: Slightly slower (but still fast - we're using in-memory SQLite)

    How it works:
    -------------
    1. Create in-memory SQLite database (sqlite:///:memory:)
    2. Create all tables (Base.metadata.create_all)
    3. Create a session for the test to use
    4. YIELD the session to the test (test runs here)
    5. Clean up: close session and drop all tables

    The "yield" keyword is the magic:
    - Everything BEFORE yield = SETUP (runs before test)
    - yield session = GIVE TO TEST
    - Everything AFTER yield = TEARDOWN (runs after test)

    Example usage in a test:
    ------------------------
    def test_create_user(db_session):  # db_session is injected automatically
        user = UserRepository.create_user(db_session, "test@example.com", ...)
        assert user.id is not None
    """
    # Setup: Create a fresh in-memory database
    engine = create_engine("sqlite:///:memory:")  # :memory: = not saved to disk
    Base.metadata.create_all(engine)  # Create all tables (User, Giftee, GiftIdea)

    # Create a session factory
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    # Provide the session to the test
    yield session

    # Teardown: Clean up after the test finishes
    session.close()
    Base.metadata.drop_all(engine)


# =============================================================================
# CONVENIENCE FIXTURES - Common Test Data
# =============================================================================

@pytest.fixture
def sample_user(db_session):
    """
    Creates a sample user for tests that need one.

    LEARNING OBJECTIVE: Fixture Composition
    ========================================
    Notice how this fixture uses "db_session" as a parameter? Pytest
    automatically handles the dependency - it will create the db_session
    FIRST, then pass it to this fixture.

    This is "fixture composition" - fixtures can depend on other fixtures!

    Why create this fixture?
    ------------------------
    Many tests need a user to exist. Instead of copying this code:

        # Without fixture (repetitive!):
        def test_create_giftee(db_session):
            user = User(email="test@example.com", ...)  # Repeated in every test
            db_session.add(user)
            db_session.commit()
            # ... rest of test

    We can use the fixture (DRY - Don't Repeat Yourself!):

        # With fixture (clean!):
        def test_create_giftee(db_session, sample_user):
            # sample_user already exists, ready to use!
            giftee = Giftee(name="Mom", user_id=sample_user.id)
            # ... rest of test

    Returns:
    --------
    User object with:
    - email: test@example.com
    - name: Test User
    - password: hashed version of "password123"
    """
    # Create user with bcrypt hashed password
    password_hash = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=password_hash
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)  # Refresh to get the auto-generated ID

    return user


@pytest.fixture
def sample_giftee(db_session, sample_user):
    """
    Creates a sample giftee for tests that need one.

    LEARNING OBJECTIVE: Multi-Level Fixture Dependencies
    =====================================================
    This fixture depends on BOTH db_session AND sample_user.
    Pytest's dependency resolution:
    1. Creates db_session (fresh database)
    2. Creates sample_user (uses db_session)
    3. Creates sample_giftee (uses both)

    Dependency chain: test → sample_giftee → sample_user → db_session

    Notice the pattern:
    -------------------
    Real app: User → Giftee → GiftIdea (hierarchy)
    Test fixtures: sample_user → sample_giftee → sample_gift_idea (same hierarchy!)

    This mirrors your domain model in your tests. Elegant!

    Returns:
    --------
    Giftee object with:
    - name: Test Giftee
    - relationship: Friend
    - budget: 100.0
    - user_id: linked to sample_user
    """
    giftee = Giftee(
        name="Test Giftee",
        relationship="Friend",
        budget=100.0,
        user_id=sample_user.id
    )

    db_session.add(giftee)
    db_session.commit()
    db_session.refresh(giftee)

    return giftee


@pytest.fixture
def sample_gift_idea(db_session, sample_giftee):
    """
    Creates a sample gift idea for tests that need one.

    LEARNING OBJECTIVE: Complete Fixture Chain
    ===========================================
    This fixture represents the full object hierarchy:
    sample_gift_idea → sample_giftee → sample_user → db_session

    When you use this fixture in a test, pytest automatically creates:
    1. A fresh database
    2. A user in that database
    3. A giftee for that user
    4. A gift idea for that giftee

    All with one line: def test_something(sample_gift_idea):

    Returns:
    --------
    GiftIdea object with:
    - title: Test Gift
    - description: A sample gift for testing
    - price: 50.0
    - rank: 1 (top priority)
    - status: considering
    - giftee_id: linked to sample_giftee
    """
    gift = GiftIdea(
        title="Test Gift",
        description="A sample gift for testing",
        price=50.0,
        rank=1,
        status="considering",
        giftee_id=sample_giftee.id
    )

    db_session.add(gift)
    db_session.commit()
    db_session.refresh(gift)

    return gift


# =============================================================================
# MULTIPLE DATA FIXTURES - For Tests Needing More Than One
# =============================================================================

@pytest.fixture
def user_with_multiple_giftees(db_session, sample_user):
    """
    Creates a user with 3 giftees for tests that need multiple.

    LEARNING OBJECTIVE: Realistic Test Scenarios
    =============================================
    Some tests need to verify behavior with MULTIPLE items:
    - Budget calculations across several giftees
    - Filtering/sorting operations
    - Pagination
    - Aggregate queries

    This fixture provides a realistic scenario: a user managing gifts
    for multiple people.

    Returns:
    --------
    Dictionary with:
    {
        'user': User object,
        'giftees': [giftee1, giftee2, giftee3]  # List of 3 Giftee objects
    }

    Example usage:
    --------------
    def test_total_budget_multiple_giftees(user_with_multiple_giftees):
        user = user_with_multiple_giftees['user']
        giftees = user_with_multiple_giftees['giftees']

        total = GifteeRepository.get_total_budget(db_session, user.id)
        assert total == 250.0  # 100 + 75 + 75
    """
    giftee1 = Giftee(
        name="Alice",
        relationship="Sister",
        budget=100.0,
        user_id=sample_user.id
    )
    giftee2 = Giftee(
        name="Bob",
        relationship="Brother",
        budget=75.0,
        user_id=sample_user.id
    )
    giftee3 = Giftee(
        name="Carol",
        relationship="Friend",
        budget=75.0,
        user_id=sample_user.id
    )

    db_session.add_all([giftee1, giftee2, giftee3])
    db_session.commit()

    # Refresh to get IDs
    db_session.refresh(giftee1)
    db_session.refresh(giftee2)
    db_session.refresh(giftee3)

    return {
        'user': sample_user,
        'giftees': [giftee1, giftee2, giftee3]
    }


@pytest.fixture
def giftee_with_multiple_gifts(db_session, sample_giftee):
    """
    Creates a giftee with 4 gifts in different statuses.

    LEARNING OBJECTIVE: Testing State Workflows
    ============================================
    Gift ideas go through a workflow:
    considering → acquired → wrapped → given

    This fixture provides gifts in each state so you can test:
    - Status-based filtering
    - Status transition logic
    - Budget calculations (only count acquired/wrapped/given)
    - Progress tracking

    Returns:
    --------
    Dictionary with:
    {
        'giftee': Giftee object,
        'gifts': {
            'considering': GiftIdea object,
            'acquired': GiftIdea object,
            'wrapped': GiftIdea object,
            'given': GiftIdea object
        }
    }

    Example usage:
    --------------
    def test_only_acquired_gifts_count_toward_budget(giftee_with_multiple_gifts):
        giftee = giftee_with_multiple_gifts['giftee']

        # Only acquired, wrapped, and given should count (not considering)
        total = GiftIdeaRepository.get_giftee_total_cost(db_session, giftee.id)
        assert total == 130.0  # 40 + 30 + 60 (excludes the $50 considering gift)
    """
    gift_considering = GiftIdea(
        title="Considering Gift",
        price=50.0,
        rank=1,
        status="considering",
        giftee_id=sample_giftee.id
    )

    gift_acquired = GiftIdea(
        title="Acquired Gift",
        price=40.0,
        rank=2,
        status="acquired",
        giftee_id=sample_giftee.id
    )

    gift_wrapped = GiftIdea(
        title="Wrapped Gift",
        price=30.0,
        rank=3,
        status="wrapped",
        giftee_id=sample_giftee.id
    )

    gift_given = GiftIdea(
        title="Given Gift",
        price=60.0,
        rank=4,
        status="given",
        giftee_id=sample_giftee.id
    )

    db_session.add_all([gift_considering, gift_acquired, gift_wrapped, gift_given])
    db_session.commit()

    return {
        'giftee': sample_giftee,
        'gifts': {
            'considering': gift_considering,
            'acquired': gift_acquired,
            'wrapped': gift_wrapped,
            'given': gift_given
        }
    }


# =============================================================================
# HELPER FUNCTIONS (Not Fixtures - Just Utilities)
# =============================================================================

def create_test_user(db_session, email="test@example.com", name="Test User", password="password123"):
    """
    Helper function to create a user with custom data.

    LEARNING OBJECTIVE: Fixtures vs Helper Functions
    =================================================
    What's the difference?

    FIXTURES (like sample_user above):
    - Decorated with @pytest.fixture
    - Injected into tests via parameters
    - Pytest manages their lifecycle
    - Use when: You need the SAME setup in many tests

    HELPER FUNCTIONS (like this one):
    - Regular Python functions
    - Called explicitly in tests
    - You manage when they run
    - Use when: You need VARIATIONS of the same setup

    Example - when to use which:

        # Use fixture when data is the same:
        def test_user_login(sample_user):
            # Always test@example.com, password123

        # Use helper when data varies:
        def test_duplicate_emails(db_session):
            user1 = create_test_user(db_session, email="alice@example.com")
            user2 = create_test_user(db_session, email="alice@example.com")
            # Testing duplicate email handling - need custom emails!

    Parameters:
    -----------
    db_session: SQLAlchemy session
    email: User email (default: test@example.com)
    name: User name (default: Test User)
    password: Plain password (will be hashed)

    Returns:
    --------
    User object saved to database
    """
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    user = User(
        email=email,
        name=name,
        password_hash=password_hash
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


def create_test_giftee(db_session, user_id, name="Test Giftee", relationship=None, budget=None):
    """
    Helper function to create a giftee with custom data.

    Use this when you need to create giftees with specific attributes
    that differ from the sample_giftee fixture.

    Parameters:
    -----------
    db_session: SQLAlchemy session
    user_id: ID of user who owns this giftee (required)
    name: Giftee name (default: Test Giftee)
    relationship: Relationship to user (default: None)
    budget: Budget amount (default: None)

    Returns:
    --------
    Giftee object saved to database
    """
    giftee = Giftee(
        name=name,
        relationship=relationship,
        budget=budget,
        user_id=user_id
    )

    db_session.add(giftee)
    db_session.commit()
    db_session.refresh(giftee)

    return giftee


def create_test_gift_idea(db_session, giftee_id, title="Test Gift", **kwargs):
    """
    Helper function to create a gift idea with custom data.

    Accepts any GiftIdea field as keyword argument.

    Parameters:
    -----------
    db_session: SQLAlchemy session
    giftee_id: ID of giftee this gift is for (required)
    title: Gift title (default: Test Gift)
    **kwargs: Any other GiftIdea fields (description, price, rank, status, url)

    Returns:
    --------
    GiftIdea object saved to database

    Example usage:
    --------------
    gift = create_test_gift_idea(
        db_session,
        giftee_id=123,
        title="Running Shoes",
        price=89.99,
        status="acquired"
    )
    """
    # Default values
    defaults = {
        'description': None,
        'price': None,
        'rank': 1,
        'status': 'considering',
        'url': None
    }

    # Override with provided kwargs
    defaults.update(kwargs)

    gift = GiftIdea(
        title=title,
        giftee_id=giftee_id,
        **defaults
    )

    db_session.add(gift)
    db_session.commit()
    db_session.refresh(gift)

    return gift


# =============================================================================
# PYTEST CONFIGURATION HOOKS
# =============================================================================

def pytest_configure(config):
    """
    Pytest hook that runs before test collection.

    LEARNING OBJECTIVE: Pytest Customization
    =========================================
    Pytest has "hooks" - functions that run at specific points in the
    test lifecycle. This hook runs ONCE when pytest starts.

    We use it here to register custom markers (tags for tests).
    """
    # Register custom markers for organizing tests
    config.addinivalue_line(
        "markers",
        "unit: Unit tests (fast, isolated, no external dependencies)"
    )
    config.addinivalue_line(
        "markers",
        "integration: Integration tests (slower, test multiple components together)"
    )
    config.addinivalue_line(
        "markers",
        "slow: Tests that take longer than 1 second"
    )
    config.addinivalue_line(
        "markers",
        "database: Tests that require database operations"
    )


# =============================================================================
# EDUCATIONAL NOTES - Common Patterns
# =============================================================================

"""
COMMON FIXTURE PATTERNS YOU'LL USE:
====================================

1. Basic fixture injection:
   def test_something(db_session):
       # db_session is automatically provided

2. Multiple fixtures:
   def test_something(db_session, sample_user, sample_giftee):
       # All three are provided

3. Mixing fixtures and regular parameters:
   def test_something(db_session, sample_user):
       # Fixtures injected, other data created in test

4. Using fixture return values:
   def test_something(user_with_multiple_giftees):
       user = user_with_multiple_giftees['user']
       giftees = user_with_multiple_giftees['giftees']

RUNNING SPECIFIC TESTS:
=======================

# Run all tests:
pytest

# Run with verbose output:
pytest -v

# Run only unit tests:
pytest -m unit

# Run only integration tests:
pytest -m integration

# Run tests in specific file:
pytest tests/unit/test_user_repository.py

# Run specific test function:
pytest tests/unit/test_user_repository.py::test_create_user

# See print statements:
pytest -s

# Stop after first failure:
pytest -x

# Show local variables on failure:
pytest -l

DEBUGGING TIPS:
===============

1. Use print() in tests (run with pytest -s):
   def test_something(sample_user):
       print(f"User ID: {sample_user.id}")
       print(f"User email: {sample_user.email}")

2. Use pytest's built-in debugger:
   pytest --pdb  # Drop into debugger on failure

3. Check fixture values:
   def test_something(sample_user):
       assert sample_user is not None, "Fixture didn't create user!"

4. Use descriptive assertion messages:
   assert user.email == "test@example.com", \
       f"Expected test@example.com, got {user.email}"

HAPPY TESTING! 🎉
==================
Remember: Good tests are:
- Fast (use in-memory database)
- Isolated (each test is independent)
- Repeatable (same input = same output)
- Thorough (test happy path AND edge cases)
- Readable (clear names, good comments)
"""
