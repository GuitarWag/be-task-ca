from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class AddToCartCommand:
    user_id: UUID
    item_id: UUID
    quantity: int
