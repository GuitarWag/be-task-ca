from typing import List, Optional
from uuid import UUID

from be_task_ca.domain.entities.cart_item import CartItem
from be_task_ca.ports.repositories.cart_item_repository import CartItemRepository


class InMemoryCartItemRepository(CartItemRepository):
    cart_items: List[CartItem]

    def __init__(self):
        self.cart_items = []

    async def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        return [item for item in self.cart_items if item.user_id == user_id]

    async def save(self, cart_item: CartItem) -> CartItem:
        self.cart_items.append(cart_item)
        return cart_item

    async def find_by_user_and_item(
        self, user_id: UUID, item_id: UUID
    ) -> Optional[CartItem]:
        for item in self.cart_items:
            if item.user_id == user_id and item.item_id == item_id:
                return item
        return None
