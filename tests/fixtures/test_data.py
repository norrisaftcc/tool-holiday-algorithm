"""
Test Data Factory

EDUCATIONAL NOTE FOR STUDENTS:
================================
This module provides factory functions for creating test data with
sensible defaults. Think of these as "test data builders" that make
your tests cleaner and more focused.

Why use factories instead of creating objects directly in tests?
----------------------------------------------------------------
1. DRY (Don't Repeat Yourself) - Write setup code once
2. Sensible defaults - Only specify what matters for your test
3. Flexibility - Easy to override specific fields
4. Maintenance - Change defaults in one place

The Pattern:
------------
Factory functions accept minimal required parameters and provide
defaults for everything else. Override defaults using kwargs.

Example:
    # Without factory (verbose):
    user = User(
        email="test1@example.com",
        name="Test User 1",
        password_hash=bcrypt.hashpw("password".encode(), bcrypt.gensalt())
    )

    # With factory (concise):
    user = UserFactory.create(db_session, email="test1@example.com")

Author: Holiday Gifting Dashboard Team
Purpose: Educational test data creation
"""

import bcrypt
from app.models import User, Giftee, GiftIdea
from typing import Optional
import random


# =============================================================================
# FACTORY CLASSES
# =============================================================================

class UserFactory:
    """
    Factory for creating User test objects.

    LEARNING OBJECTIVE: The Factory Pattern
    ========================================
    Instead of scattering user creation code throughout your tests,
    centralize it here. This makes tests more readable and maintainable.

    Benefits:
    - Consistent test data across all tests
    - Easy to create variations (admin user, user without email, etc.)
    - One place to update if User model changes
    """

    _counter = 0  # Class variable for unique emails

    @classmethod
    def create(
        cls,
        db_session,
        email: Optional[str] = None,
        name: str = "Test User",
        password: str = "password123"
    ) -> User:
        """
        Create a User with sensible defaults.

        Parameters:
        -----------
        db_session: SQLAlchemy session
        email: User email (auto-generated if None)
        name: User name (default: "Test User")
        password: Plain password that will be hashed (default: "password123")

        Returns:
        --------
        User object saved to database

        Example usage:
        --------------
        # Create with all defaults (auto-generated email):
        user = UserFactory.create(db_session)

        # Create with custom email:
        user = UserFactory.create(db_session, email="alice@example.com")

        # Create with custom everything:
        user = UserFactory.create(
            db_session,
            email="bob@example.com",
            name="Bob Smith",
            password="secure456"
        )
        """
        # Auto-generate unique email if not provided
        if email is None:
            cls._counter += 1
            email = f"testuser{cls._counter}@example.com"

        # Hash the password (bcrypt is slow, so we only do it when needed)
        password_hash = bcrypt.hashpw(
            password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = User(
            email=email,
            name=name,
            password_hash=password_hash
        )

        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)  # Get the auto-generated ID

        return user

    @classmethod
    def create_batch(cls, db_session, count: int = 3, **kwargs) -> list[User]:
        """
        Create multiple users at once.

        LEARNING OBJECTIVE: Batch Creation for List-Based Tests
        ========================================================
        Some tests need multiple objects (testing pagination, sorting,
        filtering, etc.). This method makes it easy.

        Parameters:
        -----------
        db_session: SQLAlchemy session
        count: Number of users to create (default: 3)
        **kwargs: Common attributes for all users

        Returns:
        --------
        List of User objects

        Example usage:
        --------------
        # Create 5 users with default data:
        users = UserFactory.create_batch(db_session, count=5)

        # Create 3 users with same name:
        users = UserFactory.create_batch(db_session, count=3, name="Test User")
        """
        users = []
        for i in range(count):
            # Each user gets unique email, but can share other attributes
            user = cls.create(db_session, **kwargs)
            users.append(user)
        return users


class GifteeFactory:
    """
    Factory for creating Giftee test objects.

    LEARNING OBJECTIVE: Factories with Required Dependencies
    =========================================================
    Unlike User (which exists independently), a Giftee MUST have a user_id.
    This factory handles that requirement elegantly.
    """

    _counter = 0

    # Realistic sample names for variety in tests
    _sample_names = [
        "Alice", "Bob", "Carol", "David", "Emma", "Frank",
        "Grace", "Henry", "Iris", "Jack", "Kate", "Leo"
    ]

    # Realistic relationships
    _sample_relationships = [
        "Mother", "Father", "Sister", "Brother", "Friend",
        "Partner", "Colleague", "Cousin", "Aunt", "Uncle"
    ]

    @classmethod
    def create(
        cls,
        db_session,
        user_id: int,
        name: Optional[str] = None,
        relationship: Optional[str] = None,
        budget: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Giftee:
        """
        Create a Giftee with sensible defaults.

        Parameters:
        -----------
        db_session: SQLAlchemy session
        user_id: ID of user who owns this giftee (REQUIRED)
        name: Giftee name (random if None)
        relationship: Relationship to user (random if None)
        budget: Budget amount (None if not specified)
        notes: Optional notes

        Returns:
        --------
        Giftee object saved to database

        Example usage:
        --------------
        # Minimal - just user_id required:
        giftee = GifteeFactory.create(db_session, user_id=user.id)

        # Custom name and budget:
        giftee = GifteeFactory.create(
            db_session,
            user_id=user.id,
            name="Mom",
            budget=150.0
        )
        """
        # Auto-generate realistic name if not provided
        if name is None:
            cls._counter += 1
            name = random.choice(cls._sample_names)
            # Make it unique if we've run out of names
            if cls._counter > len(cls._sample_names):
                name = f"{name} {cls._counter}"

        # Auto-generate realistic relationship if not provided
        if relationship is None:
            relationship = random.choice(cls._sample_relationships)

        giftee = Giftee(
            name=name,
            relationship=relationship,
            budget=budget,
            notes=notes,
            user_id=user_id
        )

        db_session.add(giftee)
        db_session.commit()
        db_session.refresh(giftee)

        return giftee

    @classmethod
    def create_batch(
        cls,
        db_session,
        user_id: int,
        count: int = 3,
        **kwargs
    ) -> list[Giftee]:
        """
        Create multiple giftees for a user.

        Example usage:
        --------------
        # Create 5 giftees for a user:
        giftees = GifteeFactory.create_batch(db_session, user_id=user.id, count=5)

        # Create 3 giftees with $100 budget each:
        giftees = GifteeFactory.create_batch(
            db_session,
            user_id=user.id,
            count=3,
            budget=100.0
        )
        """
        giftees = []
        for i in range(count):
            giftee = cls.create(db_session, user_id=user_id, **kwargs)
            giftees.append(giftee)
        return giftees


class GiftIdeaFactory:
    """
    Factory for creating GiftIdea test objects.

    LEARNING OBJECTIVE: Factories with Complex Defaults
    ====================================================
    Gift ideas have many optional fields (description, url, price, etc.)
    and a workflow status. This factory provides realistic defaults for
    common test scenarios.
    """

    _counter = 0

    # Realistic sample gift titles
    _sample_titles = [
        "Book", "Coffee Mug", "Scarf", "Plant", "Candle",
        "Board Game", "Headphones", "Wallet", "Watch", "Keychain",
        "Photo Frame", "Cookbook", "Art Print", "Blanket", "Journal"
    ]

    @classmethod
    def create(
        cls,
        db_session,
        giftee_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        price: Optional[float] = None,
        rank: int = 1,
        status: str = "considering"
    ) -> GiftIdea:
        """
        Create a GiftIdea with sensible defaults.

        Parameters:
        -----------
        db_session: SQLAlchemy session
        giftee_id: ID of giftee this gift is for (REQUIRED)
        title: Gift title (random if None)
        description: Gift description (None by default)
        url: Product URL (None by default)
        price: Price in dollars (random $20-100 if None)
        rank: Priority ranking (default: 1 = top priority)
        status: Workflow status (default: "considering")

        Returns:
        --------
        GiftIdea object saved to database

        Example usage:
        --------------
        # Minimal - just giftee_id:
        gift = GiftIdeaFactory.create(db_session, giftee_id=giftee.id)

        # Custom gift with all details:
        gift = GiftIdeaFactory.create(
            db_session,
            giftee_id=giftee.id,
            title="Running Shoes",
            description="Nike Air Zoom, size 10",
            price=89.99,
            status="acquired"
        )
        """
        # Auto-generate title if not provided
        if title is None:
            cls._counter += 1
            title = random.choice(cls._sample_titles)
            # Make unique if needed
            if cls._counter > len(cls._sample_titles):
                title = f"{title} #{cls._counter}"

        # Auto-generate realistic price if not provided
        if price is None:
            price = round(random.uniform(20.0, 100.0), 2)

        gift = GiftIdea(
            title=title,
            description=description,
            url=url,
            price=price,
            rank=rank,
            status=status,
            giftee_id=giftee_id
        )

        db_session.add(gift)
        db_session.commit()
        db_session.refresh(gift)

        return gift

    @classmethod
    def create_batch(
        cls,
        db_session,
        giftee_id: int,
        count: int = 3,
        **kwargs
    ) -> list[GiftIdea]:
        """
        Create multiple gift ideas for a giftee.

        Example usage:
        --------------
        # Create 5 random gifts:
        gifts = GiftIdeaFactory.create_batch(db_session, giftee_id=giftee.id, count=5)

        # Create 3 acquired gifts:
        gifts = GiftIdeaFactory.create_batch(
            db_session,
            giftee_id=giftee.id,
            count=3,
            status="acquired"
        )
        """
        gifts = []
        for i in range(count):
            # Auto-increment rank for each gift
            rank = kwargs.get('rank', i + 1)
            gift = cls.create(
                db_session,
                giftee_id=giftee_id,
                rank=rank,
                **{k: v for k, v in kwargs.items() if k != 'rank'}
            )
            gifts.append(gift)
        return gifts

    @classmethod
    def create_workflow_set(
        cls,
        db_session,
        giftee_id: int
    ) -> dict[str, GiftIdea]:
        """
        Create one gift in each workflow status.

        LEARNING OBJECTIVE: Testing State Machines
        ===========================================
        The gift workflow is a state machine:
        considering → acquired → wrapped → given

        This method creates a complete set for testing workflow logic,
        status filtering, or budget calculations.

        Returns:
        --------
        Dictionary mapping status to GiftIdea:
        {
            'considering': GiftIdea(...),
            'acquired': GiftIdea(...),
            'wrapped': GiftIdea(...),
            'given': GiftIdea(...)
        }

        Example usage:
        --------------
        gifts = GiftIdeaFactory.create_workflow_set(db_session, giftee_id=giftee.id)

        # Test that only acquired+ statuses count toward budget
        considering_gift = gifts['considering']
        acquired_gift = gifts['acquired']

        total = GiftIdeaRepository.get_giftee_total_cost(db_session, giftee.id)
        # Should NOT include 'considering' gift price
        """
        statuses = ['considering', 'acquired', 'wrapped', 'given']
        gifts = {}

        for i, status in enumerate(statuses):
            gift = cls.create(
                db_session,
                giftee_id=giftee_id,
                title=f"{status.title()} Gift",
                price=25.0 * (i + 1),  # $25, $50, $75, $100
                rank=i + 1,
                status=status
            )
            gifts[status] = gift

        return gifts


# =============================================================================
# CONVENIENCE FUNCTIONS - Common Test Scenarios
# =============================================================================

def create_user_with_giftees(
    db_session,
    num_giftees: int = 3,
    gifts_per_giftee: int = 2
):
    """
    Create a complete test scenario: user with multiple giftees, each with gifts.

    LEARNING OBJECTIVE: Hierarchical Test Data
    ===========================================
    Many tests need realistic scenarios with multiple levels of data.
    This function creates a complete hierarchy in one call.

    Parameters:
    -----------
    db_session: SQLAlchemy session
    num_giftees: Number of giftees to create (default: 3)
    gifts_per_giftee: Number of gifts per giftee (default: 2)

    Returns:
    --------
    Dictionary with:
    {
        'user': User object,
        'giftees': [Giftee, Giftee, ...],
        'gifts': [[GiftIdea, GiftIdea], [GiftIdea, GiftIdea], ...]
    }

    Example usage:
    --------------
    scenario = create_user_with_giftees(db_session, num_giftees=5, gifts_per_giftee=3)
    user = scenario['user']
    all_giftees = scenario['giftees']
    all_gifts = scenario['gifts']  # List of lists

    # Total number of gifts created: num_giftees * gifts_per_giftee
    total_gifts = sum(len(gifts) for gifts in all_gifts)
    assert total_gifts == 15  # 5 giftees * 3 gifts each
    """
    # Create user
    user = UserFactory.create(db_session)

    # Create giftees for this user
    giftees = GifteeFactory.create_batch(
        db_session,
        user_id=user.id,
        count=num_giftees
    )

    # Create gifts for each giftee
    all_gifts = []
    for giftee in giftees:
        gifts = GiftIdeaFactory.create_batch(
            db_session,
            giftee_id=giftee.id,
            count=gifts_per_giftee
        )
        all_gifts.append(gifts)

    return {
        'user': user,
        'giftees': giftees,
        'gifts': all_gifts
    }


# =============================================================================
# EDUCATIONAL EXAMPLES
# =============================================================================

"""
FACTORY PATTERN - EXAMPLE USAGE IN TESTS
=========================================

Example 1: Simple Test with Factory
------------------------------------
def test_user_can_login(db_session):
    # Create user with factory
    user = UserFactory.create(db_session, email="alice@example.com")

    # Test login logic
    result = UserRepository.get_user_by_email(db_session, "alice@example.com")
    assert result.id == user.id

Example 2: Testing with Multiple Objects
-----------------------------------------
def test_users_are_isolated(db_session):
    # Create 3 users easily
    users = UserFactory.create_batch(db_session, count=3)

    # Each should have unique email
    emails = [u.email for u in users]
    assert len(set(emails)) == 3  # All unique

Example 3: Complex Scenario
----------------------------
def test_budget_across_multiple_giftees(db_session):
    # Create complete scenario
    scenario = create_user_with_giftees(
        db_session,
        num_giftees=5,
        gifts_per_giftee=3
    )

    user = scenario['user']

    # Test budget calculation
    total = GifteeRepository.get_total_budget(db_session, user.id)
    assert total > 0

Example 4: Testing Edge Cases
------------------------------
def test_giftee_without_budget(db_session):
    user = UserFactory.create(db_session)

    # Explicitly set budget to None
    giftee = GifteeFactory.create(
        db_session,
        user_id=user.id,
        budget=None  # Edge case: no budget set
    )

    assert giftee.budget is None

BENEFITS OF FACTORIES:
======================
✅ Less boilerplate in tests
✅ Consistent test data
✅ Easy to create variations
✅ Tests focus on what they're testing (not setup)
✅ One place to maintain test data creation
✅ Realistic, randomized data for robustness

WHEN NOT TO USE FACTORIES:
==========================
❌ When testing object creation itself (test the actual constructor)
❌ When you need EXACT control over every field (be explicit instead)
❌ When testing validation (need invalid data, factories create valid data)

For those cases, create objects directly in the test with the specific
values that matter for what you're testing.
"""
