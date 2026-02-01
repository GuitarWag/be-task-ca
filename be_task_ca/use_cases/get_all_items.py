from typing import List

from be_task_ca.domain.entities.item import Item
from be_task_ca.ports.repositories.item_repository import ItemRepository


class GetAllItemsUseCase:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    async def __call__(self) -> List[Item]:
        items = await self.item_repository.list_all()
        return items
