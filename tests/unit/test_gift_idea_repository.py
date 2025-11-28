"""
Unit Tests for GiftIdeaRepository

EDUCATIONAL NOTE FOR STUDENTS:
================================
This is the most complex repository test file because GiftIdea has:
- Status workflow (considering → acquired → wrapped → given)
- Ranking/ordering (gifts have priorities)
- Price calculations (filtering by status)
- Multiple relationships (belongs to giftee, which belongs to user)

New Concepts You'll Learn:
---------------------------
1. Testing state machines (status workflows)
2. Testing ordered data (rank field)
3. Testing filtered aggregates (sum only certain statuses)
4. Testing complex queries (across multiple tables)
5. Testing business rules (which statuses count toward budget)

Prerequisites:
--------------
Complete test_user_repository.py and test_giftee_repository.py first!
This builds on all those concepts.

Author: Holiday Gifting Dashboard Team
Purpose: Advanced educational testing examples for CS students
"""

import pytest
from app.repository import GiftIdeaRepository, GifteeRepository, UserRepository
from app.models import GiftIdea
from tests.fixtures.test_data import UserFactory, GifteeFactory, GiftIdeaFactory


# =============================================================================
# TEST CLASS: Gift Idea Creation
# =============================================================================

class TestGiftIdeaCreation:
    """
    Tests for creating new gift ideas.

    LEARNING OBJECTIVE: Testing Models with Multiple Optional Fields
    =================================================================
    GiftIdea has MANY optional fields:
    - description (optional text)
    - url (optional link)
    - price (optional number)
    - rank (has default: 1)
    - status (has default: "considering")

    This teaches handling complex object creation with mixed requirements.
    """

    def test_create_gift_with_all_fields(self, db_session, sample_giftee):
        """Test creating a gift idea with all fields populated."""
        # Arrange
        gift_data = {
            'giftee_id': sample_giftee.id,
            'title': 'Running Shoes',
            'description': 'Nike Air Zoom, size 10',
            'url': 'https://example.com/shoes',
            'price': 89.99,
            'rank': 1,
            'status': 'considering'
        }

        # Act
        gift = GiftIdeaRepository.create_gift_idea(db_session, **gift_data)

        # Assert
        assert gift.id is not None
        assert gift.title == gift_data['title']
        assert gift.description == gift_data['description']
        assert gift.url == gift_data['url']
        assert gift.price == gift_data['price']
        assert gift.rank == gift_data['rank']
        assert gift.status == gift_data['status']
        assert gift.giftee_id == sample_giftee.id

    def test_create_gift_with_minimal_fields(self, db_session, sample_giftee):
        """
        Test creating a gift with only required fields.

        LEARNING: Defaults and Required Fields
        =======================================
        Required: giftee_id, title
        Defaults: rank=1, status="considering"
        Optional: description, url, price

        This tests that defaults are applied correctly.
        """
        # Arrange & Act - Only provide required fields
        gift = GiftIdeaRepository.create_gift_idea(
            db_session,
            giftee_id=sample_giftee.id,
            title="Simple Gift"
        )

        # Assert - Defaults should be applied
        assert gift.title == "Simple Gift"
        assert gift.rank == 1, "Should default to rank 1"
        assert gift.status == "considering", "Should default to 'considering' status"
        assert gift.description is None
        assert gift.url is None
        assert gift.price is None

    @pytest.mark.parametrize("status", ["considering", "acquired", "wrapped", "given"])
    def test_create_gift_with_each_valid_status(self, db_session, sample_giftee, status):
        """
        Test creating gifts in each valid status.

        LEARNING: Parametrized Tests for Enum-Like Values
        ==================================================
        The status field has a fixed set of valid values (like an enum).
        We use parametrize to test all of them efficiently.

        This pattern is common when testing:
        - Status fields
        - Role fields (admin, user, guest)
        - Type fields (credit, debit)
        - Any field with a limited set of valid values
        """
        # Act
        gift = GiftIdeaRepository.create_gift_idea(
            db_session,
            giftee_id=sample_giftee.id,
            title=f"{status.title()} Gift",
            status=status
        )

        # Assert
        assert gift.status == status


# =============================================================================
# TEST CLASS: Gift Retrieval and Ordering
# =============================================================================

class TestGiftRetrieval:
    """
    Tests for retrieving and ordering gift ideas.

    LEARNING OBJECTIVE: Testing Ordered Data
    =========================================
    Gifts have a 'rank' field (1 = highest priority).
    The get_giftee_gifts method returns gifts ordered by rank.

    Testing ordered data requires:
    1. Create multiple items with different ranks
    2. Retrieve them
    3. Verify they're in the correct order
    """

    def test_get_gift_by_id_finds_existing(self, db_session, sample_gift_idea):
        """Test retrieving a gift by ID."""
        # Act
        found = GiftIdeaRepository.get_gift_by_id(db_session, sample_gift_idea.id)

        # Assert
        assert found is not None
        assert found.id == sample_gift_idea.id
        assert found.title == sample_gift_idea.title

    def test_get_gift_by_id_returns_none_for_nonexistent(self, db_session):
        """Test retrieving a gift with invalid ID."""
        # Act
        found = GiftIdeaRepository.get_gift_by_id(db_session, 99999)

        # Assert
        assert found is None

    def test_get_giftee_gifts_returns_ordered_by_rank(self, db_session, sample_giftee):
        """
        Test that gifts are returned in rank order (1, 2, 3...).

        LEARNING: Testing Sort Order
        =============================
        When a function is supposed to return data in a specific order,
        you MUST test that the order is correct!

        Steps:
        1. Create items in RANDOM order (not sorted)
        2. Retrieve them
        3. Verify they come back SORTED
        """
        # Arrange - Create gifts in NON-sequential order
        gift_rank_3 = GiftIdeaFactory.create(
            db_session, sample_giftee.id, title="Third", rank=3
        )
        gift_rank_1 = GiftIdeaFactory.create(
            db_session, sample_giftee.id, title="First", rank=1
        )
        gift_rank_2 = GiftIdeaFactory.create(
            db_session, sample_giftee.id, title="Second", rank=2
        )

        # Act
        gifts = GiftIdeaRepository.get_giftee_gifts(db_session, sample_giftee.id)

        # Assert - Should be sorted by rank
        assert len(gifts) == 3
        assert gifts[0].rank == 1, "First gift should have rank 1"
        assert gifts[1].rank == 2, "Second gift should have rank 2"
        assert gifts[2].rank == 3, "Third gift should have rank 3"

        # Also verify by title (confirms the right gifts)
        assert gifts[0].title == "First"
        assert gifts[1].title == "Second"
        assert gifts[2].title == "Third"

    def test_get_giftee_gifts_returns_empty_for_giftee_with_no_gifts(self, db_session, sample_giftee):
        """Test retrieving gifts for a giftee who has none."""
        # Act
        gifts = GiftIdeaRepository.get_giftee_gifts(db_session, sample_giftee.id)

        # Assert
        assert gifts == []
        assert isinstance(gifts, list)


# =============================================================================
# TEST CLASS: Gift Updates
# =============================================================================

class TestGiftUpdates:
    """
    Tests for updating gift ideas.

    LEARNING OBJECTIVE: Partial Updates and Status Transitions
    ===========================================================
    Like GifteeRepository, this tests partial updates.
    Additionally, we test status transitions specifically.
    """

    def test_update_gift_title(self, db_session, sample_gift_idea):
        """Test updating the title field."""
        # Arrange
        new_title = "Updated Gift Title"

        # Act
        updated = GiftIdeaRepository.update_gift(
            db_session,
            sample_gift_idea.id,
            title=new_title
        )

        # Assert
        assert updated.title == new_title

    def test_update_gift_price(self, db_session, sample_gift_idea):
        """Test updating the price field."""
        # Arrange
        new_price = 129.99

        # Act
        updated = GiftIdeaRepository.update_gift(
            db_session,
            sample_gift_idea.id,
            price=new_price
        )

        # Assert
        assert updated.price == new_price

    def test_update_multiple_fields(self, db_session, sample_gift_idea):
        """Test updating several fields at once."""
        # Arrange
        updates = {
            'title': 'New Title',
            'description': 'New description',
            'price': 99.99,
            'rank': 2
        }

        # Act
        updated = GiftIdeaRepository.update_gift(
            db_session,
            sample_gift_idea.id,
            **updates
        )

        # Assert
        for field, value in updates.items():
            assert getattr(updated, field) == value

    def test_update_gift_status_using_update_gift_status_method(self, db_session, sample_gift_idea):
        """
        Test the dedicated update_gift_status method.

        LEARNING: Convenience Methods
        ==============================
        update_gift_status() is a convenience wrapper around update_gift().
        It exists because status updates are SO COMMON that they deserve
        their own method.

        This is good API design:
        - General method: update_gift() - for any field
        - Specific method: update_gift_status() - for common operation

        Test both to ensure they work correctly!
        """
        # Arrange
        assert sample_gift_idea.status == "considering"

        # Act
        updated = GiftIdeaRepository.update_gift_status(
            db_session,
            sample_gift_idea.id,
            "acquired"
        )

        # Assert
        assert updated.status == "acquired"

    @pytest.mark.parametrize("old_status,new_status", [
        ("considering", "acquired"),
        ("acquired", "wrapped"),
        ("wrapped", "given"),
        ("given", "considering"),  # Can go back (user changes mind)
    ])
    def test_status_transitions(self, db_session, sample_giftee, old_status, new_status):
        """
        Test all valid status transitions.

        LEARNING: Testing State Machines
        =================================
        The gift status is a STATE MACHINE. It has states and transitions:

        States: considering, acquired, wrapped, given
        Transitions: considering → acquired → wrapped → given
                    (can also go backwards if user changes mind)

        This is a common pattern in software:
        - Order status: pending → processing → shipped → delivered
        - Payment status: unpaid → processing → paid → refunded
        - User status: inactive → active → suspended → deleted

        When testing state machines:
        1. Test all valid transitions
        2. Test invalid transitions (if enforced)
        3. Test state-dependent behavior
        """
        # Arrange - Create gift in old status
        gift = GiftIdeaFactory.create(
            db_session,
            sample_giftee.id,
            title=f"{old_status} to {new_status}",
            status=old_status
        )

        # Act - Transition to new status
        updated = GiftIdeaRepository.update_gift_status(
            db_session,
            gift.id,
            new_status
        )

        # Assert
        assert updated.status == new_status


# =============================================================================
# TEST CLASS: Gift Deletion
# =============================================================================

class TestGiftDeletion:
    """
    Tests for deleting gift ideas.

    LEARNING OBJECTIVE: Simple Deletion (No Cascades)
    ==================================================
    Unlike deleting a giftee (which cascades to gifts),
    deleting a gift is straightforward - it only affects that gift.
    """

    def test_delete_gift_removes_from_database(self, db_session, sample_gift_idea):
        """Test that deleting a gift removes it."""
        # Arrange
        gift_id = sample_gift_idea.id

        # Act
        result = GiftIdeaRepository.delete_gift(db_session, gift_id)

        # Assert
        assert result is True

        # Verify deletion
        found = GiftIdeaRepository.get_gift_by_id(db_session, gift_id)
        assert found is None

    def test_delete_nonexistent_gift_returns_false(self, db_session):
        """Test deleting a gift that doesn't exist."""
        # Act
        result = GiftIdeaRepository.delete_gift(db_session, 99999)

        # Assert
        assert result is False

    def test_deleting_gift_does_not_affect_giftee(self, db_session, giftee_with_multiple_gifts):
        """
        Test that deleting a gift doesn't delete the giftee.

        LEARNING: Unidirectional Cascade
        =================================
        CASCADE DELETE works ONE WAY:
        - Delete giftee → Delete gifts ✅
        - Delete gift → Delete giftee ❌ (No!)

        Always test both directions to ensure cascades work as expected.
        """
        # Arrange
        giftee = giftee_with_multiple_gifts['giftee']
        gift_to_delete = giftee_with_multiple_gifts['gifts']['considering']

        # Act - Delete one gift
        GiftIdeaRepository.delete_gift(db_session, gift_to_delete.id)

        # Assert - Giftee should still exist
        found_giftee = GifteeRepository.get_giftee_by_id(db_session, giftee.id)
        assert found_giftee is not None, "Giftee should still exist after deleting a gift"

        # Other gifts should still exist
        remaining_gifts = GiftIdeaRepository.get_giftee_gifts(db_session, giftee.id)
        assert len(remaining_gifts) == 3, "Should have 3 gifts remaining (deleted 1 of 4)"


# =============================================================================
# TEST CLASS: Cost Calculations (Status-Based)
# =============================================================================

class TestCostCalculations:
    """
    Tests for get_giftee_total_cost() method.

    LEARNING OBJECTIVE: Status-Based Filtering and Business Logic
    ==============================================================
    This is where we test BUSINESS RULES, not just database queries!

    Business Rule: Only gifts in these statuses count toward budget:
    - acquired (you bought it)
    - wrapped (it's ready to give)
    - given (already given)

    Gifts in "considering" status DON'T count (just ideas, not purchased).

    This is business logic encoded in the repository method.
    Testing it ensures the business rules are correctly implemented!
    """

    def test_total_cost_includes_only_acquired_and_later_statuses(self, db_session, giftee_with_multiple_gifts):
        """
        Test the core business rule: only certain statuses count.

        LEARNING: Testing Business Logic
        =================================
        This is NOT testing SQL. This is testing a BUSINESS DECISION:
        "Which gift statuses should count toward the budget?"

        Answer: acquired, wrapped, given (NOT considering)

        Why? Because "considering" means "just an idea" - you haven't
        actually spent money yet.

        This test DOCUMENTS and ENFORCES that business rule.
        """
        # Arrange
        giftee = giftee_with_multiple_gifts['giftee']
        gifts = giftee_with_multiple_gifts['gifts']

        # From fixture:
        # considering: $50 (should NOT count)
        # acquired: $40 (should count)
        # wrapped: $30 (should count)
        # given: $60 (should count)
        # Expected total: $40 + $30 + $60 = $130

        # Act
        total = GiftIdeaRepository.get_giftee_total_cost(db_session, giftee.id)

        # Assert
        assert total == 130.0, \
            "Should only count acquired ($40) + wrapped ($30) + given ($60), not considering ($50)"

        # Explicitly verify considering gift is NOT counted
        considering_price = gifts['considering'].price
        assert total != considering_price + 40 + 30 + 60, \
            "Considering gift should not be included in total cost"

    def test_total_cost_zero_when_all_gifts_considering(self, db_session, sample_giftee):
        """
        Test that all 'considering' gifts result in zero total cost.

        LEARNING: Testing Edge Cases in Business Logic
        ===============================================
        What if someone adds lots of gift IDEAS but hasn't bought anything?
        Total cost should be $0 (all considering = no purchases yet).
        """
        # Arrange - Create multiple gifts, all in 'considering' status
        GiftIdeaFactory.create(db_session, sample_giftee.id, price=50.0, status="considering")
        GiftIdeaFactory.create(db_session, sample_giftee.id, price=75.0, status="considering")
        GiftIdeaFactory.create(db_session, sample_giftee.id, price=100.0, status="considering")

        # Act
        total = GiftIdeaRepository.get_giftee_total_cost(db_session, sample_giftee.id)

        # Assert
        assert total == 0.0, "All considering gifts should result in $0 total cost"

    def test_total_cost_handles_none_prices(self, db_session, sample_user):
        """
        Test that gifts without prices (None) don't break the calculation.

        LEARNING: Defensive Programming
        ================================
        Not all gifts have prices set. Maybe you haven't decided yet,
        or it's a handmade gift with no cost.

        Good code handles None values gracefully:
        - Don't crash: TypeError
        - Don't count None as zero (that's misleading)
        - Skip None values in the sum
        """
        # Arrange - Create fresh giftee with no existing gifts
        giftee = GifteeFactory.create(db_session, sample_user.id, "Test Giftee")

        # Create mix of gifts with and without prices
        # Note: Must explicitly pass price (including None) or factory assigns random price
        GiftIdeaRepository.create_gift_idea(
            db_session, giftee.id, "Gift 1", price=50.0, status="acquired"
        )
        GiftIdeaRepository.create_gift_idea(
            db_session, giftee.id, "Gift 2", price=None, status="acquired"  # No price!
        )
        GiftIdeaRepository.create_gift_idea(
            db_session, giftee.id, "Gift 3", price=30.0, status="wrapped"
        )

        # Act
        total = GiftIdeaRepository.get_giftee_total_cost(db_session, giftee.id)

        # Assert
        assert total == 80.0, "Should sum $50 + $30, ignoring the None price"

    def test_total_cost_zero_when_no_gifts(self, db_session, sample_giftee):
        """Test total cost when giftee has no gifts."""
        # Act
        total = GiftIdeaRepository.get_giftee_total_cost(db_session, sample_giftee.id)

        # Assert
        assert total == 0.0


# =============================================================================
# TEST CLASS: Cross-Repository Queries
# =============================================================================

class TestCrossRepositoryQueries:
    """
    Tests for get_user_all_gifts() method.

    LEARNING OBJECTIVE: Queries Across Multiple Tables
    ===================================================
    This method retrieves gifts across ALL of a user's giftees.
    It requires joining: User → Giftee → GiftIdea

    This is more complex than single-table queries!
    """

    def test_get_user_all_gifts_returns_all_gifts_for_user(self, db_session):
        """
        Test retrieving all gifts across all giftees for a user.

        LEARNING: Multi-Table Queries
        ==============================
        SQL logic (simplified):
        1. Find all giftees for user
        2. For each giftee, find all gifts
        3. Combine and return

        This tests the repository correctly implements that logic.
        """
        # Arrange - Create user with 2 giftees, each with 2 gifts
        user = UserFactory.create(db_session, email="multi@test.com")

        giftee1 = GifteeFactory.create(db_session, user.id, "Mom")
        gift1_1 = GiftIdeaFactory.create(db_session, giftee1.id, "Gift 1 for Mom")
        gift1_2 = GiftIdeaFactory.create(db_session, giftee1.id, "Gift 2 for Mom")

        giftee2 = GifteeFactory.create(db_session, user.id, "Dad")
        gift2_1 = GiftIdeaFactory.create(db_session, giftee2.id, "Gift 1 for Dad")
        gift2_2 = GiftIdeaFactory.create(db_session, giftee2.id, "Gift 2 for Dad")

        # Act
        all_gifts = GiftIdeaRepository.get_user_all_gifts(db_session, user.id)

        # Assert
        assert len(all_gifts) == 4, "Should return all 4 gifts across both giftees"

        # Verify all gifts belong to this user's giftees
        all_gift_ids = {g.id for g in all_gifts}
        expected_ids = {gift1_1.id, gift1_2.id, gift2_1.id, gift2_2.id}
        assert all_gift_ids == expected_ids

    def test_get_user_all_gifts_isolates_users(self, db_session):
        """
        Test that users can't see each other's gifts.

        SECURITY: Data Isolation
        ========================
        This is similar to the giftee isolation test, but at the gift level.
        User1's gifts should NOT appear in User2's results.
        """
        # Arrange - Create 2 users with gifts
        user1 = UserFactory.create(db_session, email="user1@isolation.test")
        user2 = UserFactory.create(db_session, email="user2@isolation.test")

        giftee1 = GifteeFactory.create(db_session, user1.id, "User1's Giftee")
        giftee2 = GifteeFactory.create(db_session, user2.id, "User2's Giftee")

        gift1 = GiftIdeaFactory.create(db_session, giftee1.id, "User1's Gift")
        gift2 = GiftIdeaFactory.create(db_session, giftee2.id, "User2's Gift")

        # Act
        user1_gifts = GiftIdeaRepository.get_user_all_gifts(db_session, user1.id)

        # Assert
        assert len(user1_gifts) == 1
        assert user1_gifts[0].id == gift1.id

        # Verify user2's gift is NOT in user1's results
        user1_gift_ids = [g.id for g in user1_gifts]
        assert gift2.id not in user1_gift_ids, \
            "SECURITY FAILURE: User can see other users' gifts!"

    def test_get_user_all_gifts_returns_empty_for_user_with_no_gifts(self, db_session, sample_user):
        """Test that user with no gifts returns empty list."""
        # Act
        gifts = GiftIdeaRepository.get_user_all_gifts(db_session, sample_user.id)

        # Assert
        assert gifts == []


# =============================================================================
# INTEGRATION TEST CLASS
# =============================================================================

@pytest.mark.integration
class TestGiftIdeaWorkflows:
    """
    Integration tests for complete gift idea workflows.

    LEARNING OBJECTIVE: Real-World User Journeys
    =============================================
    These tests simulate actual user behavior:
    - Add gift idea → Mark as acquired → Update price → Calculate total
    - Progress through status workflow
    - Move gifts around in priority ranking
    """

    def test_complete_gift_workflow(self, db_session):
        """
        Test the full gift lifecycle: Add → Buy → Wrap → Give

        This simulates the real user journey through the app.
        """
        # Step 1: User signs up and adds giftee
        user = UserFactory.create(db_session, email="workflow@test.com")
        giftee = GifteeRepository.create_giftee(db_session, user.id, "Mom", budget=200.0)

        # Step 2: User adds gift idea
        gift = GiftIdeaRepository.create_gift_idea(
            db_session,
            giftee.id,
            "Scarf",
            price=45.0,
            status="considering"
        )
        assert gift.status == "considering"

        # Step 3: User buys the gift
        gift = GiftIdeaRepository.update_gift_status(db_session, gift.id, "acquired")
        assert gift.status == "acquired"

        # Step 4: Check total spent
        total = GiftIdeaRepository.get_giftee_total_cost(db_session, giftee.id)
        assert total == 45.0, "Acquired gift should count toward total"

        # Step 5: User wraps the gift
        gift = GiftIdeaRepository.update_gift_status(db_session, gift.id, "wrapped")
        assert gift.status == "wrapped"

        # Step 6: User gives the gift
        gift = GiftIdeaRepository.update_gift_status(db_session, gift.id, "given")
        assert gift.status == "given"

        # Total should still include given gifts
        total = GiftIdeaRepository.get_giftee_total_cost(db_session, giftee.id)
        assert total == 45.0, "Given gifts should still count toward total"

    def test_gift_ranking_workflow(self, db_session, sample_giftee):
        """
        Test managing gift priority ranking.

        LEARNING: Testing Reordering
        =============================
        Users can change gift priorities (rank).
        This tests that rank updates work and ordering is correct.
        """
        # Step 1: Add 3 gifts
        gift1 = GiftIdeaFactory.create(db_session, sample_giftee.id, "First", rank=1)
        gift2 = GiftIdeaFactory.create(db_session, sample_giftee.id, "Second", rank=2)
        gift3 = GiftIdeaFactory.create(db_session, sample_giftee.id, "Third", rank=3)

        # Step 2: Promote gift3 to top priority
        GiftIdeaRepository.update_gift(db_session, gift3.id, rank=1)
        GiftIdeaRepository.update_gift(db_session, gift1.id, rank=2)

        # Step 3: Retrieve and verify new order
        gifts = GiftIdeaRepository.get_giftee_gifts(db_session, sample_giftee.id)

        assert gifts[0].title == "Third", "Third should now be first"
        assert gifts[1].title == "First", "First should now be second"
        assert gifts[2].title == "Second", "Second should still be last"


# =============================================================================
# EDUCATIONAL SUMMARY
# =============================================================================

"""
CONGRATULATIONS! 🎉
===================
You've completed all three repository test files!

TOTAL TEST COUNT:
- UserRepository: 19 tests
- GifteeRepository: 24 tests
- GiftIdeaRepository: 29 tests
- TOTAL: 72 comprehensive tests

KEY CONCEPTS MASTERED:
======================

FROM UserRepository:
✅ AAA Pattern
✅ Fixtures and test setup
✅ Parametrized tests
✅ Security testing (password hashing)
✅ Edge cases and graceful failures

FROM GifteeRepository:
✅ Foreign key relationships
✅ Optional fields handling
✅ Partial updates
✅ CASCADE DELETE operations
✅ Aggregate calculations (SUM)
✅ User data isolation

FROM GiftIdeaRepository (NEW):
✅ State machines (status workflows)
✅ Ordered data (rank sorting)
✅ Status-based filtering
✅ Business logic testing
✅ Cross-repository queries
✅ Complex workflows

TESTING PATTERNS YOU KNOW:
===========================
1. AAA (Arrange-Act-Assert)
2. Fixtures for setup
3. Factories for test data
4. Parametrize for variations
5. Integration for workflows
6. Edge cases and null handling
7. Security and data isolation
8. State machine testing
9. Ordered data verification
10. Business rule enforcement

REAL-WORLD APPLICATIONS:
========================
These patterns apply to:
- E-commerce (cart → checkout → payment → shipped)
- Social media (draft → published → archived)
- Task management (todo → in-progress → done)
- CRM systems (lead → prospect → customer)
- Any app with status workflows!

RUNNING ALL TESTS:
==================

# Run all repository tests:
pytest tests/unit/ -v

# Run with coverage:
pytest tests/unit/ --cov=app.repository --cov-report=html

# View coverage report:
open htmlcov/index.html

# Run only integration tests:
pytest tests/unit/ -m integration

NEXT LEVEL SKILLS:
==================
You're now ready for:
1. Mocking external APIs (AI service tests)
2. End-to-end testing (complete user flows)
3. Performance testing (load tests)
4. Test-Driven Development (TDD)

YOU ARE NOW A COMPETENT SOFTWARE TESTER! 🚀
==========================================

The tests you write will:
- Catch bugs before users find them
- Document how code should work
- Give you confidence to refactor
- Make code reviews easier
- Help new developers understand the system

Keep testing. Keep learning. Keep building! 💪
"""
