from be_task_ca.domain.entities.item import Item
from be_task_ca.ports.repositories.item_repository import ItemRepository
from be_task_ca.use_cases.commands.item_commands import CreateItemCommand
from be_task_ca.use_cases.exceptions.item_exceptions import ItemAlreadyExistsError


class CreateItemUseCase:
    def __init__(self, item_repository: ItemRepository):
        self.item_repository = item_repository

    async def __call__(self, command: CreateItemCommand) -> Item:
        existing_item = await self.item_repository.find_by_name(command.name)
        if existing_item is not None:
            raise ItemAlreadyExistsError(item_name=command.name)

        item = Item(
            name=command.name,
            description=command.description,
            price=float(command.price),
            quantity=command.quantity,
        )

        saved_item = await self.item_repository.save(item)

        return saved_item
