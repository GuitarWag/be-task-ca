from dataclasses import dataclass
from uuid import UUID


@dataclass
class CartItem:
    user_id: UUID
    item_id: UUID
    quantity: int
