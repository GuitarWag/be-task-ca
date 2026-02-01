from typing import List
from fastapi import HTTPException

from .repository import find_item_by_name, get_all_items, save_item

from .model import Item
from .schema import AllItemsRepsonse, CreateItemRequest, CreateItemResponse
from sqlalchemy.orm import Session


def create_item(item: CreateItemRequest, db: Session) -> CreateItemResponse:
    search_result = find_item_by_name(item.name, db)
    if search_result is not None:
        raise HTTPException(
            status_code=409, detail="An item with this name already exists"
        )

    new_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )

    save_item(new_item, db)
    return model_to_schema(new_item)


def get_all(db: Session) -> List[CreateItemResponse]:
    item_list = get_all_items(db)
    return AllItemsRepsonse(items=list(map(model_to_schema, item_list)))


def model_to_schema(item: Item) -> CreateItemResponse:
    return CreateItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )
