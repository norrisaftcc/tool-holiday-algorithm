"""
Data models for Holiday Gifting Dashboard.
Investigator: Clive
Case File: Database Schema
"""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship as sa_relationship
from pydantic import BaseModel, Field

# SQLAlchemy ORM Setup
Base = declarative_base()


class User(Base):
    """User account model."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    giftees = sa_relationship("Giftee", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"


class Giftee(Base):
    """Person receiving a gift."""
    __tablename__ = "giftees"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    relationship = Column(String(100), nullable=True)  # Partner, Parent, Friend, etc.
    budget = Column(Float, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = sa_relationship("User", back_populates="giftees")
    gifts = sa_relationship("GiftIdea", back_populates="giftee", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Giftee(id={self.id}, name='{self.name}', user_id={self.user_id})>"


class GiftIdea(Base):
    """Gift idea for a giftee."""
    __tablename__ = "gift_ideas"

    id = Column(Integer, primary_key=True)
    giftee_id = Column(Integer, ForeignKey("giftees.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=True)  # Link to product
    price = Column(Float, nullable=True)
    rank = Column(Integer, default=1, nullable=False)  # 1 = top choice
    status = Column(String(20), default="considering", nullable=False)  # considering, acquired, wrapped, given
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    giftee = sa_relationship("Giftee", back_populates="gifts")

    def __repr__(self):
        return f"<GiftIdea(id={self.id}, title='{self.title}', status='{self.status}')>"


# Pydantic Models for API/UI (validation and serialization)

class UserBase(BaseModel):
    """Base user data."""
    email: str
    name: str


class UserCreate(UserBase):
    """User creation schema."""
    password: str


class UserRead(UserBase):
    """User read schema."""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GifteeBase(BaseModel):
    """Base giftee data."""
    name: str
    relationship: Optional[str] = None
    budget: Optional[float] = None
    notes: Optional[str] = None


class GifteeCreate(GifteeBase):
    """Giftee creation schema."""
    pass


class GifteeUpdate(GifteeBase):
    """Giftee update schema."""
    pass


class GifteeRead(GifteeBase):
    """Giftee read schema with gifts."""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GiftIdeaBase(BaseModel):
    """Base gift idea data."""
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    price: Optional[float] = None
    rank: int = Field(default=1, ge=1)
    status: str = Field(default="considering")


class GiftIdeaCreate(GiftIdeaBase):
    """Gift idea creation schema."""
    pass


class GiftIdeaUpdate(BaseModel):
    """Gift idea update schema (partial)."""
    title: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    price: Optional[float] = None
    rank: Optional[int] = None
    status: Optional[str] = None


class GiftIdeaRead(GiftIdeaBase):
    """Gift idea read schema."""
    id: int
    giftee_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class GifteeWithGifts(GifteeRead):
    """Giftee with all their gift ideas."""
    gifts: List[GiftIdeaRead] = []

    class Config:
        from_attributes = True
