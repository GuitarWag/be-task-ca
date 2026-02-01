from uuid import UUID
from typing import List, Optional
from abc import ABC, abstractmethod

from be_task_ca.domain.entities.item import Item


class ItemRepository(ABC):
    @abstractmethod
    async def save(self, item: Item) -> Item:
        pass

    @abstractmethod
    async def list_all(self) -> List[Item]:
        pass

    @abstractmethod
    async def find_by_name(self, item_name: str) -> Optional[Item]:
        pass

    @abstractmethod
    async def find_by_id(self, item_id: UUID) -> Optional[Item]:
        pass
