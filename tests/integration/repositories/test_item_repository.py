import pytest
from uuid import uuid4

from be_task_ca.adapters.repositories.item.in_memory_item_repository import InMemoryItemRepository
from be_task_ca.domain.entities.item import Item


@pytest.fixture
def item_repository():
    return InMemoryItemRepository()


@pytest.fixture
def sample_item():
    return Item(
        name="Laptop",
        description="High-performance laptop",
        price=999.99,
        quantity=10
    )


@pytest.fixture
def another_item():
    return Item(
        name="Mouse",
        description="Wireless mouse",
        price=29.99,
        quantity=50
    )


@pytest.mark.asyncio
async def test_save_item(item_repository, sample_item):
    result = await item_repository.save(sample_item)

    assert result == sample_item
    assert result.id == sample_item.id
    assert result.name == "Laptop"
    assert result.price == 999.99


@pytest.mark.asyncio
async def test_save_multiple_items(item_repository, sample_item, another_item):
    await item_repository.save(sample_item)
    await item_repository.save(another_item)

    assert len(item_repository.items) == 2


@pytest.mark.asyncio
async def test_list_all_returns_all_items(item_repository, sample_item, another_item):
    await item_repository.save(sample_item)
    await item_repository.save(another_item)

    items = await item_repository.list_all()

    assert len(items) == 2
    assert sample_item in items
    assert another_item in items


@pytest.mark.asyncio
async def test_list_all_empty_repository(item_repository):
    items = await item_repository.list_all()

    assert items == []


@pytest.mark.asyncio
async def test_list_all_returns_copy(item_repository, sample_item):
    await item_repository.save(sample_item)

    items = await item_repository.list_all()
    items.clear()

    assert len(item_repository.items) == 1


@pytest.mark.asyncio
async def test_find_by_name_exact_match(item_repository, sample_item):
    await item_repository.save(sample_item)

    found = await item_repository.find_by_name("Laptop")

    assert found is not None
    assert found.name == "Laptop"
    assert found.id == sample_item.id


@pytest.mark.asyncio
async def test_find_by_name_case_insensitive(item_repository, sample_item):
    await item_repository.save(sample_item)

    found = await item_repository.find_by_name("laptop")

    assert found is not None
    assert found.name == "Laptop"


@pytest.mark.asyncio
async def test_find_by_name_case_insensitive_uppercase(item_repository, sample_item):
    await item_repository.save(sample_item)

    found = await item_repository.find_by_name("LAPTOP")

    assert found is not None
    assert found.name == "Laptop"


@pytest.mark.asyncio
async def test_find_by_name_not_found(item_repository):
    found = await item_repository.find_by_name("NonExistentItem")

    assert found is None


@pytest.mark.asyncio
async def test_find_by_name_returns_first_match(item_repository, sample_item, another_item):
    await item_repository.save(sample_item)
    await item_repository.save(another_item)

    found = await item_repository.find_by_name("Laptop")

    assert found == sample_item


@pytest.mark.asyncio
async def test_find_by_id_exact_match(item_repository, sample_item):
    await item_repository.save(sample_item)

    found = await item_repository.find_by_id(sample_item.id)

    assert found is not None
    assert found.id == sample_item.id
    assert found.name == "Laptop"


@pytest.mark.asyncio
async def test_find_by_id_not_found(item_repository):
    fake_id = uuid4()

    found = await item_repository.find_by_id(fake_id)

    assert found is None


@pytest.mark.asyncio
async def test_find_by_id_returns_correct_item(item_repository, sample_item, another_item):
    await item_repository.save(sample_item)
    await item_repository.save(another_item)

    found = await item_repository.find_by_id(another_item.id)

    assert found == another_item
    assert found.name == "Mouse"


@pytest.mark.asyncio
async def test_data_persistence_after_save(item_repository, sample_item):
    await item_repository.save(sample_item)

    assert len(item_repository.items) == 1
    assert item_repository.items[0] == sample_item


@pytest.mark.asyncio
async def test_saved_item_has_id(item_repository):
    item = Item(
        name="Keyboard",
        description="Mechanical keyboard",
        price=149.99,
        quantity=25
    )

    saved_item = await item_repository.save(item)

    assert saved_item.id is not None


@pytest.mark.asyncio
async def test_find_by_name_with_multiple_items_different_names(item_repository):
    item1 = Item(
        name="Monitor",
        description="4K Monitor",
        price=499.99,
        quantity=5
    )
    item2 = Item(
        name="Keyboard",
        description="Mechanical keyboard",
        price=149.99,
        quantity=20
    )

    await item_repository.save(item1)
    await item_repository.save(item2)

    found_monitor = await item_repository.find_by_name("Monitor")
    found_keyboard = await item_repository.find_by_name("Keyboard")

    assert found_monitor.name == "Monitor"
    assert found_keyboard.name == "Keyboard"
    assert found_monitor.id != found_keyboard.id


@pytest.mark.asyncio
async def test_list_all_with_multiple_saves(item_repository):
    items = [
        Item(name="Item1", description="Desc1", price=10.0, quantity=1),
        Item(name="Item2", description="Desc2", price=20.0, quantity=2),
        Item(name="Item3", description="Desc3", price=30.0, quantity=3),
    ]

    for item in items:
        await item_repository.save(item)

    all_items = await item_repository.list_all()

    assert len(all_items) == 3
    assert all(item in all_items for item in items)
