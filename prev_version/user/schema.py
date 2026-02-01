from typing import List
from uuid import UUID
from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    shipping_address: str | None


class CreateUserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str
    shipping_address: str | None


class AddToCartRequest(BaseModel):
    item_id: UUID
    quantity: int


class AddToCartResponse(BaseModel):
    items: List[AddToCartRequest]
