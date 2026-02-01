from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from .model import Item


def save_item(item: Item, db: Session) -> Item:
    db.add(item)
    db.commit()
    return item


def get_all_items(db: Session) -> List[Item]:
    return db.query(Item).all()


def find_item_by_name(name: str, db: Session) -> Item:
    return db.query(Item).filter(Item.name == name).first()


def find_item_by_id(id: UUID, db: Session) -> Item:
    return db.query(Item).filter(Item.id == id).first()
