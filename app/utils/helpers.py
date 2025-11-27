"""
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
    return f"{colors['emoji']} {status.capitalize()}"
