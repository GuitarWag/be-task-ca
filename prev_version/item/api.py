from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .usecases import create_item, get_all

from ..common import get_db

from .schema import CreateItemRequest, CreateItemResponse


item_router = APIRouter(
    prefix="/items",
    tags=["item"],
)


@item_router.post("/")
async def post_item(
    item: CreateItemRequest, db: Session = Depends(get_db)
) -> CreateItemResponse:
    return create_item(item, db)


@item_router.get("/")
async def get_items(db: Session = Depends(get_db)):
    return get_all(db)
