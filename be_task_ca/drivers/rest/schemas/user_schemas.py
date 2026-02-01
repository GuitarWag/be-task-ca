from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)
    shipping_address: str | None = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    shipping_address: str
