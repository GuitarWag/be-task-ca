from uuid import UUID


class ItemAlreadyInCartError(Exception):
    def __init__(self, user_id: UUID, item_id: UUID):
        self.user_id = user_id
        self.item_id = item_id
        super().__init__(f"Item {item_id} already in cart for user {user_id}")
