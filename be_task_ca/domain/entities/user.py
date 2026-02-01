from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from be_task_ca.domain.entities.cart_item import CartItem


@dataclass
class User:
    email: str
    first_name: str
    last_name: str
    hashed_password: str
    shipping_address: str
    cart_items: List["CartItem"] = field(default_factory=list)
    id: UUID = field(default_factory=uuid4)
