from uuid import UUID
from pydantic import BaseModel, Field


class CreateItemRequest(BaseModel):
    name: str = Field(..., min_length=1)
    description: str
    price: float = Field(..., gt=0)
    quantity: int = Field(..., ge=0)


class ItemResponse(BaseModel):
    id: UUID
    name: str
    description: str
    price: float
    quantity: int
