#!/usr/bin/env python3
"""
Database initialization script - sets up tables and creates test data.
Investigator: Clive
Case File: Database Initialization
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import init_db, get_db, close_db
from app.repository import UserRepository, GifteeRepository, GiftIdeaRepository


def main():
    """Initialize database and create sample data."""
    print("\n" + "="*60)
    print("🎁 Holiday Gifting Dashboard - Database Initialization")
    print("="*60 + "\n")

    # Initialize database
    print("Step 1: Creating database tables...")
    init_db()
    print("✓ Database tables created successfully\n")

    # Create sample user
    print("Step 2: Creating sample user...")
    db = get_db()
    try:
        # Check if demo user already exists
        demo_user = UserRepository.get_user_by_email(db, "demo@example.com")
        if not demo_user:
            demo_user = UserRepository.create_user(
                db,
                email="demo@example.com",
                name="Demo User",
                password="demo123"
            )
            print(f"✓ Created demo user: {demo_user.email}\n")
        else:
            print(f"✓ Demo user already exists: {demo_user.email}\n")

        # Create sample giftees
        print("Step 3: Creating sample giftees...")
        giftees_data = [
            {
                "name": "Alice Johnson",
                "relationship": "Partner",
                "budget": 150.0,
                "notes": "Loves tea and reading"
            },
            {
                "name": "Bob Smith",
                "relationship": "Friend",
                "budget": 50.0,
                "notes": "Tech enthusiast"
            }
        ]

        sample_giftees = []
        existing_giftees = GifteeRepository.get_user_giftees(db, demo_user.id)
        existing_giftee_names = [g.name for g in existing_giftees]

        for giftee_data in giftees_data:
            if giftee_data["name"] not in existing_giftee_names:
                giftee = GifteeRepository.create_giftee(
                    db,
                    demo_user.id,
                    **giftee_data
                )
                sample_giftees.append(giftee)
                print(f"  ✓ Created giftee: {giftee.name}")
            else:
                # Find and add existing giftee
                for g in existing_giftees:
                    if g.name == giftee_data["name"]:
                        sample_giftees.append(g)
                        print(f"  ✓ Giftee already exists: {g.name}")

        # Create sample gifts
        print("\nStep 4: Creating sample gift ideas...")
        gifts_by_giftee = {
            "Alice Johnson": [
                {
                    "title": "Premium Tea Set",
                    "description": "Ceramic tea set with infuser",
                    "price": 60.0,
                    "rank": 1,
                    "status": "considering",
                    "url": "https://example.com/tea-set"
                },
                {
                    "title": "Book: The Midnight Library",
                    "description": "New release, highly recommended",
                    "price": 20.0,
                    "rank": 2,
                    "status": "considering"
                }
            ],
            "Bob Smith": [
                {
                    "title": "USB-C Hub",
                    "description": "7-in-1 multiport adapter",
                    "price": 45.0,
                    "rank": 1,
                    "status": "acquired",
                    "url": "https://example.com/usb-hub"
                }
            ]
        }

        for giftee in sample_giftees:
            if giftee.name in gifts_by_giftee:
                for gift_data in gifts_by_giftee[giftee.name]:
                    # Check if gift already exists
                    existing_gifts = GiftIdeaRepository.get_giftee_gifts(db, giftee.id)
                    gift_exists = any(g.title == gift_data["title"] for g in existing_gifts)

                    if not gift_exists:
                        gift = GiftIdeaRepository.create_gift_idea(
                            db,
                            giftee.id,
                            **gift_data
                        )
                        print(f"  ✓ Created gift for {giftee.name}: {gift.title}")
                    else:
                        print(f"  ✓ Gift already exists for {giftee.name}: {gift_data['title']}")

    finally:
        close_db(db)

    print("\n" + "="*60)
    print("✅ Database initialization complete!")
    print("="*60)
    print("\nYou can now log in with:")
    print("  Email: demo@example.com")
    print("  Password: demo123")
    print("\nStart the app with: streamlit run app/main.py")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
