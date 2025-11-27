"""
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
