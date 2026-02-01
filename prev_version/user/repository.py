from uuid import UUID
from sqlalchemy.orm import Session
from .model import CartItem, User


def save_user(user: User, db: Session):
    db.add(user)
    db.commit()
    return user


def find_user_by_email(email: str, db: Session):
    return db.query(User).filter(User.email == email).first()


def find_user_by_id(user_id: UUID, db: Session):
    return db.query(User).filter(User.id == user_id).first()


def find_cart_items_for_user_id(user_id, db):
    return db.query(CartItem).filter(CartItem.user_id == user_id).all()
