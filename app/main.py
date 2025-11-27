"""
Holiday Gifting Dashboard - Main Application Entry Point
Investigator: Clive
Case: Rapid MVP Development - Ready for Deployment
"""

import streamlit as st
from pathlib import Path
import sys
import os

# Add app to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db, get_db, close_db
from app.repository import UserRepository, GifteeRepository, GiftIdeaRepository
from app.config import SESSION_KEYS, APP_NAME, EMPTY_STATES
from app.utils.helpers import calculate_progress, format_currency, render_status_badge
from app.services.ai_service import GiftBrainstormingService, GiftScenario

# Configure Streamlit page
st.set_page_config(
    page_title=APP_NAME,
    page_icon="🎁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize database
init_db()

# Session state initialization
if SESSION_KEYS["user"] not in st.session_state:
    st.session_state[SESSION_KEYS["user"]] = False
    st.session_state[SESSION_KEYS["user_id"]] = None
    st.session_state[SESSION_KEYS["user_email"]] = None
    st.session_state[SESSION_KEYS["user_name"]] = None


def login_user(email: str, password: str) -> bool:
    """Authenticate user and set session."""
    db = get_db()
    try:
        user = UserRepository.get_user_by_email(db, email)
        if user and UserRepository.verify_password(password, user.password_hash):
            st.session_state[SESSION_KEYS["user"]] = True
            st.session_state[SESSION_KEYS["user_id"]] = user.id
            st.session_state[SESSION_KEYS["user_email"]] = user.email
            st.session_state[SESSION_KEYS["user_name"]] = user.name
            return True
        return False
    finally:
        close_db(db)


def register_user(email: str, name: str, password: str) -> tuple[bool, str]:
    """Register a new user."""
    db = get_db()
    try:
        if UserRepository.user_exists(db, email):
            return False, "Email already registered"

        UserRepository.create_user(db, email, name, password)
        return True, "Registration successful! Please log in."
    except Exception as e:
        return False, f"Registration error: {str(e)}"
    finally:
        close_db(db)


def logout_user():
    """Log out current user."""
    st.session_state[SESSION_KEYS["user"]] = False
    st.session_state[SESSION_KEYS["user_id"]] = None
    st.session_state[SESSION_KEYS["user_email"]] = None
    st.session_state[SESSION_KEYS["user_name"]] = None


def auth_page():
    """Authentication page - login and registration."""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.title("🎁 Holiday Gifting Dashboard")
        st.markdown("---")

        auth_tab1, auth_tab2 = st.tabs(["Login", "Register"])

        with auth_tab1:
            st.subheader("Login")
            login_email = st.text_input(
                "Email",
                key="login_email"
            )
            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button("Login", use_container_width=True):
                if login_email and login_password:
                    if login_user(login_email, login_password):
                        st.success("Logged in successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
                else:
                    st.warning("Please enter email and password")

        with auth_tab2:
            st.subheader("Create Account")
            reg_name = st.text_input(
                "Full Name",
                key="reg_name"
            )
            reg_email = st.text_input(
                "Email",
                key="reg_email"
            )
            reg_password = st.text_input(
                "Password",
                type="password",
                key="reg_password"
            )
            reg_password_confirm = st.text_input(
                "Confirm Password",
                type="password",
                key="reg_password_confirm"
            )

            if st.button("Register", use_container_width=True):
                if not all([reg_name, reg_email, reg_password, reg_password_confirm]):
                    st.warning("Please fill in all fields")
                elif reg_password != reg_password_confirm:
                    st.error("Passwords do not match")
                elif len(reg_password) < 6:
                    st.error("Password must be at least 6 characters")
                else:
                    success, message = register_user(reg_email, reg_name, reg_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)


def dashboard_page():
    """Main dashboard page."""
    st.title(f"🎁 Holiday Gifting Dashboard")

    # Header with user info and logout
    col1, col2, col3 = st.columns([2, 1, 1])
    with col3:
        st.write(f"Welcome, {st.session_state[SESSION_KEYS['user_name']]}")
        if st.button("Logout"):
            logout_user()
            st.rerun()

    st.markdown("---")

    # Get user's giftees
    db = get_db()
    try:
        user_id = st.session_state[SESSION_KEYS["user_id"]]
        giftees = GifteeRepository.get_user_giftees(db, user_id)

        # Add new giftee section
        with st.expander("Add New Giftee", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Giftee Name")
                new_relationship = st.selectbox(
                    "Relationship (optional)",
                    options=["", "Partner", "Parent", "Sibling", "Child", "Friend", "Coworker", "Extended Family", "Other"]
                )
            with col2:
                new_budget = st.number_input("Budget (optional)", min_value=0.0, step=10.0)
                new_notes = st.text_area("Notes (optional)", height=50)

            if st.button("Add Giftee", use_container_width=True):
                if new_name:
                    GifteeRepository.create_giftee(
                        db,
                        user_id,
                        new_name,
                        relationship=new_relationship if new_relationship else None,
                        budget=new_budget if new_budget > 0 else None,
                        notes=new_notes if new_notes else None
                    )
                    st.success(f"Added {new_name} to your list!")
                    st.rerun()
                else:
                    st.error("Please enter a name")

        st.markdown("---")

        # Display giftees
        if giftees:
            # Overall stats
            all_gifts = GiftIdeaRepository.get_user_all_gifts(db, user_id)
            progress = calculate_progress(
                [{"status": g.status} for g in all_gifts]
            )

            st.subheader("Overall Progress")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Gifts", progress["total"])
            with col2:
                st.metric("Acquired", progress["acquired"])
            with col3:
                st.metric("Wrapped", progress["wrapped"])
            with col4:
                st.metric("Given", f"{progress['percentage']:.0f}%")

            st.markdown("---")

            # Display each giftee
            for giftee in giftees:
                with st.expander(f"🎁 {giftee.name}", expanded=True):
                    col1, col2, col3 = st.columns([2, 1, 1])

                    with col1:
                        if giftee.relationship:
                            st.write(f"**Relationship:** {giftee.relationship}")
                        if giftee.budget:
                            st.write(f"**Budget:** {format_currency(giftee.budget)}")
                        if giftee.notes:
                            st.write(f"**Notes:** {giftee.notes}")

                    with col3:
                        if st.button("Edit", key=f"edit_{giftee.id}"):
                            st.session_state[f"edit_{giftee.id}"] = True
                        if st.button("Delete", key=f"delete_{giftee.id}"):
                            GifteeRepository.delete_giftee(db, giftee.id)
                            st.rerun()

                    st.markdown("---")

                    # Gift ideas for this giftee
                    gifts = GiftIdeaRepository.get_giftee_gifts(db, giftee.id)

                    # Add gift idea section
                    with st.form(f"gift_form_{giftee.id}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            gift_title = st.text_input(
                                "Gift Idea",
                                key=f"gift_title_{giftee.id}"
                            )
                            gift_price = st.number_input(
                                "Price",
                                min_value=0.0,
                                step=1.0,
                                key=f"gift_price_{giftee.id}"
                            )
                        with col2:
                            gift_rank = st.number_input(
                                "Priority (1=top)",
                                min_value=1,
                                value=1,
                                key=f"gift_rank_{giftee.id}"
                            )
                            gift_status = st.selectbox(
                                "Status",
                                options=["considering", "acquired", "wrapped", "given"],
                                key=f"gift_status_{giftee.id}"
                            )

                        gift_description = st.text_area(
                            "Description (optional)",
                            key=f"gift_desc_{giftee.id}"
                        )
                        gift_url = st.text_input(
                            "Product Link (optional)",
                            key=f"gift_url_{giftee.id}"
                        )

                        if st.form_submit_button("Add Gift Idea", use_container_width=True):
                            if gift_title:
                                GiftIdeaRepository.create_gift_idea(
                                    db,
                                    giftee.id,
                                    gift_title,
                                    description=gift_description if gift_description else None,
                                    url=gift_url if gift_url else None,
                                    price=gift_price if gift_price > 0 else None,
                                    rank=gift_rank,
                                    status=gift_status
                                )
                                st.success(f"Added gift idea: {gift_title}")
                                st.rerun()
                            else:
                                st.error("Please enter a gift title")

                    # AI Gift Suggestions
                    st.markdown("---")
                    with st.expander("✨ Get AI Gift Suggestions", expanded=False):
                        # Check if API key is configured
                        api_key = os.getenv("CLAUDE_API_KEY") or st.session_state.get("claude_api_key")

                        if not api_key:
                            st.info("🔑 Add your Claude API key in Settings (top right) to enable AI gift suggestions")
                            st.caption("Need an API key? Visit https://console.anthropic.com")
                        else:
                            # Scenario selection
                            scenarios = GiftBrainstormingService(api_key).get_available_scenarios()

                            scenario_options = {s["label"]: s["value"] for s in scenarios}
                            selected_scenario_label = st.selectbox(
                                "Choose brainstorming scenario:",
                                options=list(scenario_options.keys()),
                                help="Different scenarios ask different questions to give you better suggestions"
                            )
                            selected_scenario = GiftScenario(scenario_options[selected_scenario_label])

                            # Context gathering based on scenario
                            context = {
                                "relationship": giftee.relationship or "someone special",
                                "budget": f"${giftee.budget}" if giftee.budget else "flexible",
                            }

                            col1, col2 = st.columns(2)
                            with col1:
                                context["interests"] = st.text_area(
                                    "Their interests/hobbies:",
                                    value=giftee.notes or "",
                                    help="What do they enjoy doing?",
                                    key=f"ai_interests_{giftee.id}"
                                )

                            with col2:
                                if selected_scenario == GiftScenario.BUDGET:
                                    context["values"] = st.text_input(
                                        "What matters most to them:",
                                        help="Values, priorities, or what they care about",
                                        key=f"ai_values_{giftee.id}"
                                    )
                                elif selected_scenario == GiftScenario.LAST_MINUTE:
                                    context["days_until_event"] = st.selectbox(
                                        "Days until you need the gift:",
                                        options=["1-2", "3-5", "6-10"],
                                        key=f"ai_days_{giftee.id}"
                                    )
                                elif selected_scenario == GiftScenario.DIY:
                                    context["your_skills"] = st.text_input(
                                        "Your crafting/DIY skills:",
                                        help="e.g., basic crafting, woodworking, baking",
                                        key=f"ai_skills_{giftee.id}"
                                    )
                                    context["time_available"] = st.text_input(
                                        "Time you can spend:",
                                        value="A few hours",
                                        key=f"ai_time_{giftee.id}"
                                    )
                                else:
                                    context["gift_preferences"] = st.text_input(
                                        "Gift preferences:",
                                        help="Practical, sentimental, experiences, etc.",
                                        key=f"ai_prefs_{giftee.id}"
                                    )

                            num_ideas = st.slider(
                                "Number of suggestions:",
                                min_value=3,
                                max_value=8,
                                value=5,
                                key=f"ai_num_{giftee.id}"
                            )

                            if st.button("✨ Generate Suggestions", key=f"ai_gen_{giftee.id}", use_container_width=True):
                                with st.spinner("Thinking of perfect gifts..."):
                                    ai_service = GiftBrainstormingService(api_key)
                                    result = ai_service.brainstorm_gifts(
                                        scenario=selected_scenario,
                                        giftee_name=giftee.name,
                                        context=context,
                                        num_ideas=num_ideas
                                    )

                                    if result["success"]:
                                        st.success(f"Generated {len(result['ideas'])} gift ideas! (Cost: ~{result['cost_estimate']})")

                                        for i, idea in enumerate(result['ideas'], 1):
                                            with st.container():
                                                col_idea, col_add = st.columns([4, 1])

                                                with col_idea:
                                                    st.markdown(f"**{i}. {idea['title']}**")
                                                    if idea.get('description'):
                                                        st.caption(f"📝 {idea['description']}")
                                                    if idea.get('why_it_fits'):
                                                        st.caption(f"💡 {idea['why_it_fits']}")
                                                    if idea.get('price_range'):
                                                        st.caption(f"💰 {idea['price_range']}")

                                                with col_add:
                                                    if st.button("Add", key=f"add_ai_{giftee.id}_{i}"):
                                                        # Add to gift ideas
                                                        GiftIdeaRepository.create_gift_idea(
                                                            db,
                                                            giftee.id,
                                                            idea['title'],
                                                            description=idea.get('description') or idea.get('why_it_fits'),
                                                            price=None,
                                                            rank=i,
                                                            status="considering"
                                                        )
                                                        st.success(f"Added: {idea['title']}")
                                                        st.rerun()

                                                st.markdown("---")
                                    else:
                                        st.error(result['error'])

                    st.markdown("---")

                    # Display existing gifts
                    if gifts:
                        st.subheader("Gift Ideas")
                        for gift in gifts:
                            gift_col1, gift_col2, gift_col3 = st.columns([2, 1, 1])

                            with gift_col1:
                                st.write(f"**{gift.title}** {render_status_badge(gift.status)}")
                                if gift.description:
                                    st.write(f"*{gift.description}*")
                                if gift.price:
                                    st.write(f"Price: {format_currency(gift.price)}")
                                if gift.url:
                                    st.write(f"[View Product]({gift.url})")

                            with gift_col2:
                                new_status = st.selectbox(
                                    "Status",
                                    options=["considering", "acquired", "wrapped", "given"],
                                    value=gift.status,
                                    key=f"status_{gift.id}"
                                )
                                if new_status != gift.status:
                                    GiftIdeaRepository.update_gift_status(db, gift.id, new_status)
                                    st.rerun()

                            with gift_col3:
                                if st.button("Delete", key=f"delete_gift_{gift.id}"):
                                    GiftIdeaRepository.delete_gift(db, gift.id)
                                    st.rerun()
                    else:
                        st.info(EMPTY_STATES["no_gifts"])

        else:
            st.info(EMPTY_STATES["no_giftees"])

    finally:
        close_db(db)


# Main app logic
def main():
    """Main application entry point."""
    if st.session_state[SESSION_KEYS["user"]]:
        dashboard_page()
    else:
        auth_page()


if __name__ == "__main__":
    main()
