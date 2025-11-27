"""
Data access layer (repository pattern) for database operations.
Investigator: Clive
Case File: Data Access
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from app.models import User, Giftee, GiftIdea
import bcrypt


class UserRepository:
    """User data access operations."""

    @staticmethod
    def create_user(db: Session, email: str, name: str, password: str) -> User:
        """Create a new user."""
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user = User(email=email, name=name, password_hash=password_hash)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def user_exists(db: Session, email: str) -> bool:
        """Check if user exists."""
        return db.query(User).filter(User.email == email).first() is not None


class GifteeRepository:
    """Giftee data access operations."""

    @staticmethod
    def create_giftee(
        db: Session,
        user_id: int,
        name: str,
        relationship: Optional[str] = None,
        budget: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Giftee:
        """Create a new giftee."""
        giftee = Giftee(
            user_id=user_id,
            name=name,
            relationship=relationship,
            budget=budget,
            notes=notes
        )
        db.add(giftee)
        db.commit()
        db.refresh(giftee)
        return giftee

    @staticmethod
    def get_giftee_by_id(db: Session, giftee_id: int) -> Optional[Giftee]:
        """Get giftee by ID."""
        return db.query(Giftee).filter(Giftee.id == giftee_id).first()

    @staticmethod
    def get_user_giftees(db: Session, user_id: int) -> List[Giftee]:
        """Get all giftees for a user."""
        return db.query(Giftee).filter(Giftee.user_id == user_id).all()

    @staticmethod
    def update_giftee(
        db: Session,
        giftee_id: int,
        **kwargs
    ) -> Optional[Giftee]:
        """Update giftee details."""
        giftee = db.query(Giftee).filter(Giftee.id == giftee_id).first()
        if giftee:
            for key, value in kwargs.items():
                if hasattr(giftee, key) and value is not None:
                    setattr(giftee, key, value)
            db.commit()
            db.refresh(giftee)
        return giftee

    @staticmethod
    def delete_giftee(db: Session, giftee_id: int) -> bool:
        """Delete a giftee and their gifts."""
        giftee = db.query(Giftee).filter(Giftee.id == giftee_id).first()
        if giftee:
            db.delete(giftee)
            db.commit()
            return True
        return False

    @staticmethod
    def get_total_budget(db: Session, user_id: int) -> float:
        """Get total budget for all giftees."""
        giftees = GifteeRepository.get_user_giftees(db, user_id)
        return sum(g.budget for g in giftees if g.budget is not None)


class GiftIdeaRepository:
    """Gift idea data access operations."""

    @staticmethod
    def create_gift_idea(
        db: Session,
        giftee_id: int,
        title: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        price: Optional[float] = None,
        rank: int = 1,
        status: str = "considering"
    ) -> GiftIdea:
        """Create a new gift idea."""
        gift = GiftIdea(
            giftee_id=giftee_id,
            title=title,
            description=description,
            url=url,
            price=price,
            rank=rank,
            status=status
        )
        db.add(gift)
        db.commit()
        db.refresh(gift)
        return gift

    @staticmethod
    def get_gift_by_id(db: Session, gift_id: int) -> Optional[GiftIdea]:
        """Get gift idea by ID."""
        return db.query(GiftIdea).filter(GiftIdea.id == gift_id).first()

    @staticmethod
    def get_giftee_gifts(db: Session, giftee_id: int) -> List[GiftIdea]:
        """Get all gift ideas for a giftee, ordered by rank."""
        return db.query(GiftIdea).filter(
            GiftIdea.giftee_id == giftee_id
        ).order_by(GiftIdea.rank).all()

    @staticmethod
    def update_gift(
        db: Session,
        gift_id: int,
        **kwargs
    ) -> Optional[GiftIdea]:
        """Update gift idea details."""
        gift = db.query(GiftIdea).filter(GiftIdea.id == gift_id).first()
        if gift:
            for key, value in kwargs.items():
                if hasattr(gift, key) and value is not None:
                    setattr(gift, key, value)
            db.commit()
            db.refresh(gift)
        return gift

    @staticmethod
    def delete_gift(db: Session, gift_id: int) -> bool:
        """Delete a gift idea."""
        gift = db.query(GiftIdea).filter(GiftIdea.id == gift_id).first()
        if gift:
            db.delete(gift)
            db.commit()
            return True
        return False

    @staticmethod
    def update_gift_status(db: Session, gift_id: int, status: str) -> Optional[GiftIdea]:
        """Update gift status."""
        return GiftIdeaRepository.update_gift(db, gift_id, status=status)

    @staticmethod
    def get_giftee_total_cost(db: Session, giftee_id: int) -> float:
        """Get total cost of acquired gifts for a giftee."""
        gifts = GiftIdeaRepository.get_giftee_gifts(db, giftee_id)
        acquired_gifts = [g for g in gifts if g.status in ["acquired", "wrapped", "given"]]
        return sum(g.price for g in acquired_gifts if g.price is not None)

    @staticmethod
    def get_user_all_gifts(db: Session, user_id: int) -> List[GiftIdea]:
        """Get all gifts for all giftees of a user."""
        giftees = db.query(Giftee).filter(Giftee.user_id == user_id).all()
        all_gifts = []
        for giftee in giftees:
            all_gifts.extend(GiftIdeaRepository.get_giftee_gifts(db, giftee.id))
        return all_gifts
