from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class Item:
    name: str
    description: str
    price: float
    quantity: int
    id: UUID = field(default_factory=uuid4)
