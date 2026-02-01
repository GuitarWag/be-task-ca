from uuid import UUID
from pydantic import BaseModel, Field


class AddToCartRequest(BaseModel):
    item_id: UUID
    quantity: int = Field(..., gt=0)


class CartItemResponse(BaseModel):
    user_id: UUID
    item_id: UUID
    quantity: int
