"""
Database connection and session management.
Investigator: Clive
Case File: Database Operations
"""

import os
from pathlib import Path
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from app.models import Base

# Get database URL from environment or use default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{Path(__file__).parent.parent / 'data' / 'holiday_gifts.db'}"
)

# Configure engine based on database type
if DATABASE_URL.startswith("sqlite"):
    # SQLite configuration for development
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=False  # Set to True for SQL debugging
    )
else:
    # PostgreSQL or other database configuration
    engine = create_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True
    )

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def init_db():
    """Initialize the database - create all tables."""
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")


def get_db() -> Session:
    """Get a database session."""
    return SessionLocal()


def close_db(db: Session):
    """Close a database session."""
    if db:
        db.close()


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    inspector = inspect(engine)
    return table_name in inspector.get_table_names()


def reset_db():
    """Drop all tables and recreate them. WARNING: Destructive operation."""
    Base.metadata.drop_all(bind=engine)
    init_db()
    print("Database reset complete.")
