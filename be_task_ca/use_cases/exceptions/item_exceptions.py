from uuid import UUID


class ItemNotFoundError(Exception):
    def __init__(self, item_id: UUID | None = None, item_name: str | None = None):
        self.item_id = item_id
        self.item_name = item_name
        if item_id:
            super().__init__(f"Item {item_id} not found")
        elif item_name:
            super().__init__(f"Item '{item_name}' not found")
        else:
            super().__init__("Item not found")


class ItemAlreadyExistsError(Exception):
    def __init__(self, item_name: str):
        self.item_name = item_name
        super().__init__(f"Item '{item_name}' already exists")


class InsufficientStockError(Exception):
    def __init__(self, item_id: UUID, requested: int, available: int):
        self.item_id = item_id
        self.requested = requested
        self.available = available
        msg = (
            f"Insufficient stock for item {item_id}: "
            f"requested {requested}, available {available}"
        )
        super().__init__(msg)
