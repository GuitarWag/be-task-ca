from typing import List, Optional
from uuid import UUID

from be_task_ca.domain.entities.item import Item
from be_task_ca.ports.repositories.item_repository import ItemRepository


class InMemoryItemRepository(ItemRepository):
    items: List[Item]

    def __init__(self):
        self.items = []

    async def save(self, item: Item) -> Item:
        self.items.append(item)
        return item

    async def list_all(self) -> List[Item]:
        return self.items.copy()

    async def find_by_name(self, item_name: str) -> Optional[Item]:
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None

    async def find_by_id(self, item_id: UUID) -> Optional[Item]:
        for item in self.items:
            if item.id == item_id:
                return item
        return None
