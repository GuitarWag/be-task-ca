from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from be_task_ca.domain.entities.item import Item
from be_task_ca.use_cases.commands.item_commands import CreateItemCommand
from be_task_ca.use_cases.exceptions.item_exceptions import ItemAlreadyExistsError
from be_task_ca.use_cases.create_item import CreateItemUseCase


@pytest.fixture
def item_repository():
    return AsyncMock()


@pytest.fixture
def create_item_use_case(item_repository):
    return CreateItemUseCase(item_repository)


@pytest.mark.asyncio
async def test_create_item_successfully(create_item_use_case, item_repository):
    command = CreateItemCommand(
        name="Laptop",
        description="High-performance laptop",
        price=999.99,
        quantity=10,
    )

    item = Item(
        id=uuid4(),
        name=command.name,
        description=command.description,
        price=float(command.price),
        quantity=command.quantity,
    )

    item_repository.find_by_name.return_value = None
    item_repository.save.return_value = item

    result = await create_item_use_case(command)

    assert result.name == "Laptop"
    assert result.description == "High-performance laptop"
    assert result.price == 999.99
    assert result.quantity == 10
    item_repository.find_by_name.assert_called_once_with("Laptop")
    item_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_item_with_zero_quantity(create_item_use_case, item_repository):
    command = CreateItemCommand(
        name="Out of Stock Item",
        description="Item with zero quantity",
        price=50.0,
        quantity=0,
    )

    item = Item(
        id=uuid4(),
        name=command.name,
        description=command.description,
        price=float(command.price),
        quantity=command.quantity,
    )

    item_repository.find_by_name.return_value = None
    item_repository.save.return_value = item

    result = await create_item_use_case(command)

    assert result.quantity == 0
    item_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_item_with_float_price(create_item_use_case, item_repository):
    command = CreateItemCommand(
        name="Product",
        description="A product",
        price=19.99,
        quantity=5,
    )

    item = Item(
        id=uuid4(),
        name=command.name,
        description=command.description,
        price=19.99,
        quantity=command.quantity,
    )

    item_repository.find_by_name.return_value = None
    item_repository.save.return_value = item

    result = await create_item_use_case(command)

    assert result.price == 19.99
    assert isinstance(result.price, float)


@pytest.mark.asyncio
async def test_create_item_item_already_exists(create_item_use_case, item_repository):
    command = CreateItemCommand(
        name="Existing Item",
        description="Item that already exists",
        price=100.0,
        quantity=5,
    )

    existing_item = Item(
        id=uuid4(),
        name="Existing Item",
        description="Item that already exists",
        price=100.0,
        quantity=5,
    )

    item_repository.find_by_name.return_value = existing_item

    with pytest.raises(ItemAlreadyExistsError):
        await create_item_use_case(command)

    item_repository.find_by_name.assert_called_once_with("Existing Item")
    item_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_item_converts_price_to_float(create_item_use_case, item_repository):
    command = CreateItemCommand(
        name="Item",
        description="Description",
        price=100,
        quantity=5,
    )

    item = Item(
        id=uuid4(),
        name=command.name,
        description=command.description,
        price=float(command.price),
        quantity=command.quantity,
    )

    item_repository.find_by_name.return_value = None
    item_repository.save.return_value = item

    result = await create_item_use_case(command)

    assert isinstance(result.price, float)
    assert result.price == 100.0
