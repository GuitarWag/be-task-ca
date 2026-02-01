from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from be_task_ca.domain.entities.item import Item
from be_task_ca.use_cases.get_all_items import GetAllItemsUseCase


@pytest.fixture
def item_repository():
    return AsyncMock()


@pytest.fixture
def get_all_items_use_case(item_repository):
    return GetAllItemsUseCase(item_repository)


@pytest.mark.asyncio
async def test_get_all_items_returns_list(get_all_items_use_case, item_repository):
    item1 = Item(
        id=uuid4(),
        name="Item 1",
        description="Description 1",
        price=10.0,
        quantity=5,
    )
    item2 = Item(
        id=uuid4(),
        name="Item 2",
        description="Description 2",
        price=20.0,
        quantity=10,
    )

    item_repository.list_all.return_value = [item1, item2]

    result = await get_all_items_use_case()

    assert len(result) == 2
    assert result[0].name == "Item 1"
    assert result[1].name == "Item 2"
    item_repository.list_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_items_returns_empty_list(get_all_items_use_case, item_repository):
    item_repository.list_all.return_value = []

    result = await get_all_items_use_case()

    assert result == []
    item_repository.list_all.assert_called_once()


@pytest.mark.asyncio
async def test_get_all_items_returns_single_item(get_all_items_use_case, item_repository):
    item = Item(
        id=uuid4(),
        name="Single Item",
        description="Only item",
        price=50.0,
        quantity=1,
    )

    item_repository.list_all.return_value = [item]

    result = await get_all_items_use_case()

    assert len(result) == 1
    assert result[0].name == "Single Item"


@pytest.mark.asyncio
async def test_get_all_items_preserves_item_properties(get_all_items_use_case, item_repository):
    item = Item(
        id=uuid4(),
        name="Test Item",
        description="Test Description",
        price=99.99,
        quantity=25,
    )

    item_repository.list_all.return_value = [item]

    result = await get_all_items_use_case()

    assert result[0].id == item.id
    assert result[0].name == item.name
    assert result[0].description == item.description
    assert result[0].price == item.price
    assert result[0].quantity == item.quantity
