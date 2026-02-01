from dataclasses import dataclass


@dataclass(frozen=True)
class CreateItemCommand:
    name: str
    description: str
    price: float
    quantity: int
