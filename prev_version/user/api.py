from uuid import UUID
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..common import get_db

from .usecases import add_item_to_cart, create_user, list_items_in_cart

from .schema import AddToCartRequest, CreateUserRequest


user_router = APIRouter(
    prefix="/users",
    tags=["user"],
)


@user_router.post("/")
async def post_customer(user: CreateUserRequest, db: Session = Depends(get_db)):
    return create_user(user, db)


@user_router.post("/{user_id}/cart")
async def post_cart(
    user_id: UUID, cart_item: AddToCartRequest, db: Session = Depends(get_db)
):
    return add_item_to_cart(user_id, cart_item, db)


@user_router.get("/{user_id}/cart")
async def get_cart(user_id: UUID, db: Session = Depends(get_db)):
    return list_items_in_cart(user_id, db)
