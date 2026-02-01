from typing import List
from uuid import UUID
from pydantic import BaseModel


class CreateItemRequest(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int


class CreateItemResponse(CreateItemRequest):
    id: UUID


class AllItemsRepsonse(BaseModel):
    items: List[CreateItemResponse]
