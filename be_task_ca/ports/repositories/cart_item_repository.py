from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from be_task_ca.domain.entities.cart_item import CartItem


class CartItemRepository(ABC):
    @abstractmethod
    async def find_cart_items_for_user_id(self, user_id: UUID) -> List[CartItem]:
        pass

    @abstractmethod
    async def save(self, cart_item: CartItem) -> CartItem:
        pass

    @abstractmethod
    async def find_by_user_and_item(
        self, user_id: UUID, item_id: UUID
    ) -> Optional[CartItem]:
        pass
