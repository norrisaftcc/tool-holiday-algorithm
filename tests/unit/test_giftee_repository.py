"""
Unit Tests for GifteeRepository

EDUCATIONAL NOTE FOR STUDENTS:
================================
Building on what you learned from test_user_repository.py, this file
demonstrates testing a more complex repository with:
- Foreign key relationships (giftee belongs to user)
- Optional fields (budget, relationship, notes)
- Cascade operations (deleting giftee deletes gifts)
- Aggregate functions (calculating total budgets)

New Concepts You'll Learn:
---------------------------
1. Testing relationships between models
2. Testing optional/nullable fields
3. Testing update operations with partial data
4. Testing delete operations with cascading effects
5. Testing aggregate calculations across multiple records

Prerequisites:
--------------
Complete test_user_repository.py first! This builds on those concepts.

Author: Holiday Gifting Dashboard Team
Purpose: Educational testing example for CS students
"""

import pytest
from app.repository import GifteeRepository, UserRepository
from app.models import Giftee
from tests.fixtures.test_data import UserFactory, GifteeFactory


# =============================================================================
# TEST CLASS: Giftee Creation
# =============================================================================

class TestGifteeCreation:
    """
    Tests for creating new giftees.

    LEARNING OBJECTIVE: Testing Models with Foreign Keys
    =====================================================
    Unlike User (which exists independently), a Giftee MUST have a user_id.
    This is a FOREIGN KEY relationship - every giftee belongs to a user.

    When testing models with foreign keys, we must:
    1. Create the parent object first (User)
    2. Use the parent's ID for the foreign key
    3. Test that invalid foreign keys are rejected
    """

    def test_create_giftee_with_all_fields(self, db_session, sample_user):
        """
        Test creating a giftee with all optional fields populated.

        LEARNING: Testing with Complete Data
        =====================================
        This is the "happy path" - everything works perfectly.
        We provide all fields including optional ones.
        """
        # Arrange
        user_id = sample_user.id
        name = "Mom"
        relationship = "Mother"
        budget = 150.0
        notes = "Likes gardening and mystery novels"

        # Act
        giftee = GifteeRepository.create_giftee(
            db_session,
            user_id=user_id,
            name=name,
            relationship=relationship,
            budget=budget,
            notes=notes
        )

        # Assert
        assert giftee is not None
        assert giftee.id is not None, "Should have database-generated ID"
        assert giftee.user_id == user_id
        assert giftee.name == name
        assert giftee.relationship == relationship
        assert giftee.budget == budget
        assert giftee.notes == notes

    def test_create_giftee_with_minimal_fields(self, db_session, sample_user):
        """
        Test creating a giftee with only required fields.

        LEARNING: Testing Optional Fields
        ==================================
        Some fields are REQUIRED (user_id, name).
        Others are OPTIONAL (relationship, budget, notes).

        This tests that the optional fields can be omitted.
        They should default to None.
        """
        # Arrange
        user_id = sample_user.id
        name = "Alice"

        # Act - Only provide required fields
        giftee = GifteeRepository.create_giftee(
            db_session,
            user_id=user_id,
            name=name
            # relationship, budget, notes intentionally omitted
        )

        # Assert
        assert giftee is not None
        assert giftee.id is not None
        assert giftee.user_id == user_id
        assert giftee.name == name
        # Optional fields should be None
        assert giftee.relationship is None
        assert giftee.budget is None
        assert giftee.notes is None

    def test_create_giftee_with_zero_budget(self, db_session, sample_user):
        """
        Test creating a giftee with budget of 0.

        LEARNING: Testing Edge Cases with Numbers
        ==========================================
        Zero is a valid budget (maybe you're making everything yourself!).
        This is different from None (no budget set).

        Always test boundary values:
        - Zero
        - Negative numbers (should these be allowed?)
        - Very large numbers
        """
        # Arrange & Act
        giftee = GifteeRepository.create_giftee(
            db_session,
            user_id=sample_user.id,
            name="DIY Giftee",
            budget=0.0  # Zero is valid!
        )

        # Assert
        assert giftee.budget == 0.0, "Zero should be stored correctly, not converted to None"
        assert giftee.budget is not None, "Zero budget is different from no budget (None)"

    def test_multiple_giftees_for_same_user(self, db_session, sample_user):
        """
        Test that one user can have multiple giftees.

        LEARNING: One-to-Many Relationships
        ====================================
        In our database:
        - One User can have MANY Giftees (one-to-many)
        - Each Giftee belongs to ONE User (many-to-one)

        This is a fundamental database relationship pattern.
        """
        # Arrange & Act - Create 3 giftees for the same user
        giftee1 = GifteeRepository.create_giftee(
            db_session, sample_user.id, "Mom"
        )
        giftee2 = GifteeRepository.create_giftee(
            db_session, sample_user.id, "Dad"
        )
        giftee3 = GifteeRepository.create_giftee(
            db_session, sample_user.id, "Sister"
        )

        # Assert - All should belong to the same user
        assert giftee1.user_id == sample_user.id
        assert giftee2.user_id == sample_user.id
        assert giftee3.user_id == sample_user.id

        # All should have unique IDs
        assert giftee1.id != giftee2.id != giftee3.id


# =============================================================================
# TEST CLASS: Giftee Retrieval
# =============================================================================

class TestGifteeRetrieval:
    """
    Tests for retrieving existing giftees.

    LEARNING OBJECTIVE: Testing Queries with Filters
    =================================================
    Unlike simple "get by ID", we also test:
    - Getting all giftees for a specific user
    - Ensuring users can't see other users' giftees
    - Handling empty result sets
    """

    def test_get_giftee_by_id_finds_existing(self, db_session, sample_giftee):
        """Test retrieving a giftee by ID when it exists."""
        # Arrange - sample_giftee fixture created a giftee

        # Act
        found = GifteeRepository.get_giftee_by_id(db_session, sample_giftee.id)

        # Assert
        assert found is not None
        assert found.id == sample_giftee.id
        assert found.name == sample_giftee.name

    def test_get_giftee_by_id_returns_none_for_nonexistent(self, db_session):
        """Test retrieving a giftee with ID that doesn't exist."""
        # Act
        found = GifteeRepository.get_giftee_by_id(db_session, 99999)

        # Assert
        assert found is None, "Should return None for non-existent ID"

    def test_get_user_giftees_returns_all_for_user(self, db_session, user_with_multiple_giftees):
        """
        Test retrieving all giftees for a specific user.

        LEARNING: Testing Filtered Queries
        ===================================
        This tests a query with a WHERE clause:
        SELECT * FROM giftees WHERE user_id = ?

        Important to verify:
        - Returns ALL matching records
        - Returns ONLY matching records (not other users' giftees)
        - Returns empty list if no matches
        """
        # Arrange
        user = user_with_multiple_giftees['user']
        expected_giftees = user_with_multiple_giftees['giftees']

        # Act
        retrieved_giftees = GifteeRepository.get_user_giftees(db_session, user.id)

        # Assert
        assert len(retrieved_giftees) == len(expected_giftees), \
            "Should return all giftees for this user"

        # Verify all belong to the correct user
        for giftee in retrieved_giftees:
            assert giftee.user_id == user.id

        # Verify we got the expected giftees
        retrieved_ids = {g.id for g in retrieved_giftees}
        expected_ids = {g.id for g in expected_giftees}
        assert retrieved_ids == expected_ids

    def test_get_user_giftees_returns_empty_for_user_with_none(self, db_session, sample_user):
        """
        Test retrieving giftees for a user who has none.

        LEARNING: Testing Empty Result Sets
        ====================================
        This is an important edge case: what happens when the query
        returns no rows?

        Good design: Return empty list [], not None
        Bad design: Crash or return None (requires null checking everywhere)
        """
        # Arrange - sample_user has no giftees created yet

        # Act
        giftees = GifteeRepository.get_user_giftees(db_session, sample_user.id)

        # Assert
        assert giftees == [], "Should return empty list, not None"
        assert isinstance(giftees, list), "Should be a list type"

    def test_user_isolation_cannot_see_other_users_giftees(self, db_session):
        """
        Test that users can only see their own giftees.

        SECURITY TESTING: Data Isolation
        =================================
        This is a CRITICAL security test! Users should NEVER be able
        to see other users' data.

        Imagine if you could see everyone else's Christmas gift lists.
        That would ruin the surprise (and violate privacy!).
        """
        # Arrange - Create two users with giftees
        user1 = UserFactory.create(db_session, email="user1@test.com")
        user2 = UserFactory.create(db_session, email="user2@test.com")

        giftee1 = GifteeRepository.create_giftee(db_session, user1.id, "User1's Mom")
        giftee2 = GifteeRepository.create_giftee(db_session, user2.id, "User2's Dad")

        # Act - Get user1's giftees
        user1_giftees = GifteeRepository.get_user_giftees(db_session, user1.id)

        # Assert - Should only see their own giftee
        assert len(user1_giftees) == 1
        assert user1_giftees[0].id == giftee1.id
        assert user1_giftees[0].name == "User1's Mom"

        # Should NOT see user2's giftee
        user1_giftee_ids = [g.id for g in user1_giftees]
        assert giftee2.id not in user1_giftee_ids, \
            "SECURITY FAILURE: User can see other users' giftees!"


# =============================================================================
# TEST CLASS: Giftee Updates
# =============================================================================

class TestGifteeUpdates:
    """
    Tests for updating existing giftees.

    LEARNING OBJECTIVE: Testing UPDATE Operations
    ==============================================
    Updates are trickier than creates because:
    1. Need to handle partial updates (only some fields changed)
    2. Need to preserve unchanged fields
    3. Need to handle updates to non-existent records
    """

    def test_update_giftee_name(self, db_session, sample_giftee):
        """
        Test updating just the name field.

        LEARNING: Partial Updates
        ==========================
        Often you want to update ONE field without touching the others.
        This tests that unchanged fields stay unchanged.
        """
        # Arrange
        original_name = sample_giftee.name
        new_name = "Updated Name"
        original_budget = sample_giftee.budget

        # Act
        updated = GifteeRepository.update_giftee(
            db_session,
            sample_giftee.id,
            name=new_name
        )

        # Assert
        assert updated.name == new_name, "Name should be updated"
        assert updated.budget == original_budget, "Budget should be unchanged"

    def test_update_giftee_budget(self, db_session, sample_giftee):
        """Test updating the budget field."""
        # Arrange
        new_budget = 200.0

        # Act
        updated = GifteeRepository.update_giftee(
            db_session,
            sample_giftee.id,
            budget=new_budget
        )

        # Assert
        assert updated.budget == new_budget

    def test_update_multiple_fields(self, db_session, sample_giftee):
        """
        Test updating several fields at once.

        LEARNING: Multi-Field Updates
        ==============================
        The update_giftee function uses **kwargs to accept any combination
        of fields. This tests that pattern.
        """
        # Arrange
        updates = {
            'name': 'New Name',
            'relationship': 'Best Friend',
            'budget': 175.0,
            'notes': 'Updated notes'
        }

        # Act
        updated = GifteeRepository.update_giftee(
            db_session,
            sample_giftee.id,
            **updates  # ** unpacks dictionary into keyword arguments
        )

        # Assert
        assert updated.name == updates['name']
        assert updated.relationship == updates['relationship']
        assert updated.budget == updates['budget']
        assert updated.notes == updates['notes']

    def test_update_nonexistent_giftee_returns_none(self, db_session):
        """
        Test updating a giftee that doesn't exist.

        LEARNING: Graceful Failure
        ===========================
        What should happen if you try to update something that doesn't exist?
        Options:
        1. Return None (graceful)
        2. Raise exception (explicit error)
        3. Silently fail (BAD - don't do this!)

        Our code chooses option 1 - return None.
        """
        # Act
        result = GifteeRepository.update_giftee(
            db_session,
            99999,  # Non-existent ID
            name="Won't Work"
        )

        # Assert
        assert result is None, "Should return None for non-existent giftee"

    def test_update_with_none_values(self, db_session):
        """
        Test that None values in update are handled correctly.

        LEARNING: Implementation Details
        ================================
        Look at the update_giftee implementation:
        ```python
        if hasattr(giftee, key) and value is not None:
            setattr(giftee, key, value)
        ```

        It only updates if value is not None. This means you can't use
        update to SET a field TO None. This is a design decision!

        This test documents that behavior.
        """
        # Arrange
        giftee = GifteeFactory.create(
            db_session,
            user_id=UserFactory.create(db_session).id,
            budget=100.0
        )
        original_budget = giftee.budget

        # Act - Try to update budget to None
        updated = GifteeRepository.update_giftee(
            db_session,
            giftee.id,
            budget=None
        )

        # Assert - Budget should be unchanged (None is ignored)
        assert updated.budget == original_budget, \
            "update_giftee ignores None values (by design)"


# =============================================================================
# TEST CLASS: Giftee Deletion
# =============================================================================

class TestGifteeDeletion:
    """
    Tests for deleting giftees.

    LEARNING OBJECTIVE: Testing DELETE with Cascades
    =================================================
    Deletion is risky! When you delete a giftee:
    - What happens to their gift ideas?
    - Can you accidentally delete someone else's giftee?
    - What if the giftee doesn't exist?

    Our database has CASCADE DELETE configured:
    When giftee is deleted, their gifts are automatically deleted too.
    """

    def test_delete_giftee_removes_from_database(self, db_session, sample_giftee):
        """
        Test that deleting a giftee actually removes it.

        LEARNING: Verifying Deletion
        =============================
        After calling delete, we need to verify:
        1. Delete operation returns True (success)
        2. Giftee can no longer be found in database
        """
        # Arrange
        giftee_id = sample_giftee.id

        # Act
        result = GifteeRepository.delete_giftee(db_session, giftee_id)

        # Assert
        assert result is True, "Delete should return True for successful deletion"

        # Verify giftee is gone
        found = GifteeRepository.get_giftee_by_id(db_session, giftee_id)
        assert found is None, "Deleted giftee should no longer exist in database"

    def test_delete_nonexistent_giftee_returns_false(self, db_session):
        """
        Test deleting a giftee that doesn't exist.

        LEARNING: Idempotent Operations
        ================================
        Deleting something that doesn't exist should:
        - Not crash (graceful handling)
        - Return False (indicate nothing was deleted)
        - Not affect other data
        """
        # Act
        result = GifteeRepository.delete_giftee(db_session, 99999)

        # Assert
        assert result is False, "Should return False when nothing to delete"

    def test_delete_giftee_with_gifts_cascades(self, db_session, giftee_with_multiple_gifts):
        """
        Test that deleting a giftee also deletes their gift ideas.

        LEARNING: CASCADE DELETE
        ========================
        This is DATABASE CASCADE behavior. When configured in the schema:

        ```python
        gifts = relationship("GiftIdea", cascade="all, delete-orphan")
        ```

        When you delete a giftee, SQLAlchemy automatically deletes all
        their related gifts.

        This prevents "orphaned" records (gifts with no giftee).
        """
        # Arrange
        giftee = giftee_with_multiple_gifts['giftee']
        gifts = giftee_with_multiple_gifts['gifts']
        giftee_id = giftee.id

        # Verify gifts exist before deletion
        from app.repository import GiftIdeaRepository
        before_delete = GiftIdeaRepository.get_giftee_gifts(db_session, giftee_id)
        assert len(before_delete) == 4, "Giftee should have 4 gifts before deletion"

        # Act
        GifteeRepository.delete_giftee(db_session, giftee_id)

        # Assert - Gifts should also be deleted
        after_delete = GiftIdeaRepository.get_giftee_gifts(db_session, giftee_id)
        assert len(after_delete) == 0, \
            "All gifts should be deleted when giftee is deleted (CASCADE)"


# =============================================================================
# TEST CLASS: Budget Calculations
# =============================================================================

class TestBudgetCalculations:
    """
    Tests for budget aggregate functions.

    LEARNING OBJECTIVE: Testing Calculations and Aggregates
    ========================================================
    This tests get_total_budget(), which:
    1. Queries multiple giftees
    2. Sums their budgets
    3. Handles None values (giftees with no budget set)

    This is testing BUSINESS LOGIC, not just database operations!
    """

    def test_get_total_budget_single_giftee(self, db_session, sample_user):
        """Test total budget with one giftee."""
        # Arrange
        GifteeRepository.create_giftee(
            db_session,
            sample_user.id,
            "Test Giftee",
            budget=100.0
        )

        # Act
        total = GifteeRepository.get_total_budget(db_session, sample_user.id)

        # Assert
        assert total == 100.0

    def test_get_total_budget_multiple_giftees(self, db_session, user_with_multiple_giftees):
        """
        Test total budget across multiple giftees.

        LEARNING: Testing Aggregate Functions
        ======================================
        This tests SUM across multiple records. Important to verify:
        - All values are included
        - Calculation is correct
        - Result type is correct (float, not string)
        """
        # Arrange
        user = user_with_multiple_giftees['user']
        giftees = user_with_multiple_giftees['giftees']

        # Calculate expected total (from fixture: 100 + 75 + 75 = 250)
        expected_total = sum(g.budget for g in giftees)

        # Act
        actual_total = GifteeRepository.get_total_budget(db_session, user.id)

        # Assert
        assert actual_total == expected_total
        assert actual_total == 250.0

    def test_get_total_budget_excludes_none_values(self, db_session, sample_user):
        """
        Test that giftees without budgets (None) don't break the calculation.

        LEARNING: Handling NULL Values in Aggregates
        =============================================
        What happens when you try to sum: [100, None, 50]?
        - Python would crash: TypeError
        - SQL SUM ignores NULLs automatically
        - Our code filters out None values

        This test ensures None values are handled gracefully.
        """
        # Arrange - Create giftees with and without budgets
        GifteeRepository.create_giftee(
            db_session, sample_user.id, "With Budget", budget=100.0
        )
        GifteeRepository.create_giftee(
            db_session, sample_user.id, "No Budget", budget=None
        )
        GifteeRepository.create_giftee(
            db_session, sample_user.id, "Also Budget", budget=50.0
        )

        # Act
        total = GifteeRepository.get_total_budget(db_session, sample_user.id)

        # Assert - Should sum only non-None values
        assert total == 150.0, "Should sum 100 + 50, ignoring None"

    def test_get_total_budget_zero_when_no_giftees(self, db_session, sample_user):
        """Test total budget when user has no giftees."""
        # Arrange - sample_user has no giftees

        # Act
        total = GifteeRepository.get_total_budget(db_session, sample_user.id)

        # Assert
        assert total == 0.0, "Should return 0 when no giftees exist"

    def test_get_total_budget_zero_when_all_budgets_none(self, db_session, sample_user):
        """Test total budget when all giftees have None budget."""
        # Arrange
        GifteeRepository.create_giftee(db_session, sample_user.id, "No Budget 1", budget=None)
        GifteeRepository.create_giftee(db_session, sample_user.id, "No Budget 2", budget=None)

        # Act
        total = GifteeRepository.get_total_budget(db_session, sample_user.id)

        # Assert
        assert total == 0.0, "Should return 0 when all budgets are None"


# =============================================================================
# INTEGRATION TEST CLASS
# =============================================================================

@pytest.mark.integration
class TestGifteeWorkflows:
    """
    Integration tests for complete giftee workflows.

    LEARNING OBJECTIVE: End-to-End Workflows
    =========================================
    These tests simulate real user actions:
    - Create user → Add giftee → Update budget → Check total
    - Create giftee → Add gifts → Delete giftee → Verify cascade

    Integration tests are slower but test realistic scenarios.
    """

    def test_complete_giftee_lifecycle(self, db_session):
        """
        Test the full lifecycle: Create → Read → Update → Delete

        This simulates a real user workflow:
        1. Sign up
        2. Add someone to gift list
        3. Update their budget
        4. Remove them from list
        """
        # Step 1: Create user
        user = UserFactory.create(db_session, email="lifecycle@test.com")

        # Step 2: Create giftee
        giftee = GifteeRepository.create_giftee(
            db_session,
            user.id,
            "Test Person",
            budget=100.0
        )
        assert giftee.id is not None

        # Step 3: Read giftee
        found = GifteeRepository.get_giftee_by_id(db_session, giftee.id)
        assert found is not None
        assert found.name == "Test Person"

        # Step 4: Update giftee
        updated = GifteeRepository.update_giftee(
            db_session,
            giftee.id,
            budget=150.0,
            notes="Increased budget"
        )
        assert updated.budget == 150.0

        # Step 5: Delete giftee
        deleted = GifteeRepository.delete_giftee(db_session, giftee.id)
        assert deleted is True

        # Step 6: Verify deletion
        not_found = GifteeRepository.get_giftee_by_id(db_session, giftee.id)
        assert not_found is None

    def test_multi_user_budget_tracking(self, db_session):
        """
        Test budget tracking across multiple users.

        This ensures user isolation and correct calculations
        when multiple users use the app simultaneously.
        """
        # Create 2 users with different giftees
        user1 = UserFactory.create(db_session, email="user1@budget.test")
        user2 = UserFactory.create(db_session, email="user2@budget.test")

        # User 1: 3 giftees with budgets totaling $300
        GifteeRepository.create_giftee(db_session, user1.id, "Mom", budget=100.0)
        GifteeRepository.create_giftee(db_session, user1.id, "Dad", budget=100.0)
        GifteeRepository.create_giftee(db_session, user1.id, "Sister", budget=100.0)

        # User 2: 2 giftees with budgets totaling $150
        GifteeRepository.create_giftee(db_session, user2.id, "Friend", budget=75.0)
        GifteeRepository.create_giftee(db_session, user2.id, "Coworker", budget=75.0)

        # Verify correct totals for each user
        user1_total = GifteeRepository.get_total_budget(db_session, user1.id)
        user2_total = GifteeRepository.get_total_budget(db_session, user2.id)

        assert user1_total == 300.0, "User 1 should have $300 total budget"
        assert user2_total == 150.0, "User 2 should have $150 total budget"


# =============================================================================
# EDUCATIONAL SUMMARY
# =============================================================================

"""
KEY TAKEAWAYS FROM GIFTEE REPOSITORY TESTS:
============================================

1. FOREIGN KEY RELATIONSHIPS
   - Giftee must have a valid user_id
   - One user can have many giftees
   - Test user isolation (can't see others' giftees)

2. OPTIONAL FIELDS
   - Test with all fields populated
   - Test with minimal required fields
   - Handle None vs zero correctly

3. PARTIAL UPDATES
   - Use **kwargs pattern
   - Only update provided fields
   - Preserve unchanged fields

4. CASCADE DELETES
   - Deleting giftee deletes their gifts
   - Prevents orphaned records
   - Test the cascade behavior

5. AGGREGATE CALCULATIONS
   - Handle None values gracefully
   - Test edge cases (zero giftees, all None budgets)
   - Verify correct arithmetic

6. INTEGRATION TESTING
   - Test complete workflows (CRUD lifecycle)
   - Test multi-user scenarios
   - Verify data isolation

RUNNING THESE TESTS:
====================

# Run all giftee tests:
pytest tests/unit/test_giftee_repository.py -v

# Run specific test class:
pytest tests/unit/test_giftee_repository.py::TestGifteeCreation -v

# Run with coverage:
pytest tests/unit/test_giftee_repository.py --cov=app.repository.GifteeRepository

PATTERNS YOU'VE NOW LEARNED:
============================
✅ AAA Pattern (from UserRepository tests)
✅ Fixtures and Factories
✅ Parametrized tests
✅ Foreign key relationships (NEW!)
✅ Optional fields handling (NEW!)
✅ Partial updates (NEW!)
✅ Cascade deletes (NEW!)
✅ Aggregate calculations (NEW!)

NEXT STEPS:
===========
Move on to test_gift_idea_repository.py to learn:
- Many-to-one relationships
- Status workflows (state machines)
- Ordering/ranking
- Filtering by status

You're building a complete testing skillset! 🚀
"""
