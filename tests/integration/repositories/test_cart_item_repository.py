import pytest
from uuid import uuid4

from be_task_ca.adapters.repositories.cart_item.in_memory_cart_item_repository import InMemoryCartItemRepository
from be_task_ca.domain.entities.cart_item import CartItem


@pytest.fixture
def cart_item_repository():
    return InMemoryCartItemRepository()


@pytest.fixture
def sample_cart_item():
    user_id = uuid4()
    item_id = uuid4()
    return CartItem(user_id=user_id, item_id=item_id, quantity=2)


@pytest.fixture
def another_cart_item():
    user_id = uuid4()
    item_id = uuid4()
    return CartItem(user_id=user_id, item_id=item_id, quantity=5)


@pytest.mark.asyncio
async def test_save_cart_item(cart_item_repository, sample_cart_item):
    result = await cart_item_repository.save(sample_cart_item)

    assert result == sample_cart_item
    assert result.user_id == sample_cart_item.user_id
    assert result.item_id == sample_cart_item.item_id
    assert result.quantity == 2


@pytest.mark.asyncio
async def test_save_multiple_cart_items(cart_item_repository, sample_cart_item, another_cart_item):
    await cart_item_repository.save(sample_cart_item)
    await cart_item_repository.save(another_cart_item)

    assert len(cart_item_repository.cart_items) == 2


@pytest.mark.asyncio
async def test_find_cart_items_for_user_id(cart_item_repository):
    user_id = uuid4()
    item_id1 = uuid4()
    item_id2 = uuid4()

    cart_item1 = CartItem(user_id=user_id, item_id=item_id1, quantity=1)
    cart_item2 = CartItem(user_id=user_id, item_id=item_id2, quantity=3)

    await cart_item_repository.save(cart_item1)
    await cart_item_repository.save(cart_item2)

    found = await cart_item_repository.find_cart_items_for_user_id(user_id)

    assert len(found) == 2
    assert cart_item1 in found
    assert cart_item2 in found


@pytest.mark.asyncio
async def test_find_cart_items_for_user_id_empty(cart_item_repository):
    user_id = uuid4()

    found = await cart_item_repository.find_cart_items_for_user_id(user_id)

    assert found == []


@pytest.mark.asyncio
async def test_find_cart_items_for_user_id_not_found(cart_item_repository):
    user_id1 = uuid4()
    user_id2 = uuid4()
    item_id = uuid4()

    cart_item = CartItem(user_id=user_id1, item_id=item_id, quantity=1)
    await cart_item_repository.save(cart_item)

    found = await cart_item_repository.find_cart_items_for_user_id(user_id2)

    assert found == []


@pytest.mark.asyncio
async def test_find_cart_items_for_user_id_filters_by_user(cart_item_repository):
    user_id1 = uuid4()
    user_id2 = uuid4()
    item_id1 = uuid4()
    item_id2 = uuid4()

    cart_item1 = CartItem(user_id=user_id1, item_id=item_id1, quantity=1)
    cart_item2 = CartItem(user_id=user_id2, item_id=item_id2, quantity=2)

    await cart_item_repository.save(cart_item1)
    await cart_item_repository.save(cart_item2)

    found = await cart_item_repository.find_cart_items_for_user_id(user_id1)

    assert len(found) == 1
    assert found[0] == cart_item1
    assert cart_item2 not in found


@pytest.mark.asyncio
async def test_find_by_user_and_item_exact_match(cart_item_repository):
    user_id = uuid4()
    item_id = uuid4()
    cart_item = CartItem(user_id=user_id, item_id=item_id, quantity=3)

    await cart_item_repository.save(cart_item)

    found = await cart_item_repository.find_by_user_and_item(user_id, item_id)

    assert found is not None
    assert found == cart_item
    assert found.quantity == 3


@pytest.mark.asyncio
async def test_find_by_user_and_item_not_found(cart_item_repository):
    user_id = uuid4()
    item_id = uuid4()

    found = await cart_item_repository.find_by_user_and_item(user_id, item_id)

    assert found is None


@pytest.mark.asyncio
async def test_find_by_user_and_item_wrong_user(cart_item_repository):
    user_id1 = uuid4()
    user_id2 = uuid4()
    item_id = uuid4()

    cart_item = CartItem(user_id=user_id1, item_id=item_id, quantity=1)
    await cart_item_repository.save(cart_item)

    found = await cart_item_repository.find_by_user_and_item(user_id2, item_id)

    assert found is None


@pytest.mark.asyncio
async def test_find_by_user_and_item_wrong_item(cart_item_repository):
    user_id = uuid4()
    item_id1 = uuid4()
    item_id2 = uuid4()

    cart_item = CartItem(user_id=user_id, item_id=item_id1, quantity=1)
    await cart_item_repository.save(cart_item)

    found = await cart_item_repository.find_by_user_and_item(user_id, item_id2)

    assert found is None


@pytest.mark.asyncio
async def test_find_by_user_and_item_returns_first_match(cart_item_repository):
    user_id = uuid4()
    item_id = uuid4()

    cart_item1 = CartItem(user_id=user_id, item_id=item_id, quantity=1)
    cart_item2 = CartItem(user_id=user_id, item_id=item_id, quantity=5)

    await cart_item_repository.save(cart_item1)
    await cart_item_repository.save(cart_item2)

    found = await cart_item_repository.find_by_user_and_item(user_id, item_id)

    assert found == cart_item1


@pytest.mark.asyncio
async def test_data_persistence_after_save(cart_item_repository, sample_cart_item):
    await cart_item_repository.save(sample_cart_item)

    assert len(cart_item_repository.cart_items) == 1
    assert cart_item_repository.cart_items[0] == sample_cart_item


@pytest.mark.asyncio
async def test_multiple_users_multiple_items(cart_item_repository):
    user_id1 = uuid4()
    user_id2 = uuid4()
    item_id1 = uuid4()
    item_id2 = uuid4()

    cart_item1 = CartItem(user_id=user_id1, item_id=item_id1, quantity=1)
    cart_item2 = CartItem(user_id=user_id1, item_id=item_id2, quantity=2)
    cart_item3 = CartItem(user_id=user_id2, item_id=item_id1, quantity=3)
    cart_item4 = CartItem(user_id=user_id2, item_id=item_id2, quantity=4)

    await cart_item_repository.save(cart_item1)
    await cart_item_repository.save(cart_item2)
    await cart_item_repository.save(cart_item3)
    await cart_item_repository.save(cart_item4)

    user1_items = await cart_item_repository.find_cart_items_for_user_id(user_id1)
    user2_items = await cart_item_repository.find_cart_items_for_user_id(user_id2)

    assert len(user1_items) == 2
    assert len(user2_items) == 2


@pytest.mark.asyncio
async def test_find_by_user_and_item_with_multiple_combinations(cart_item_repository):
    user_id1 = uuid4()
    user_id2 = uuid4()
    item_id1 = uuid4()
    item_id2 = uuid4()

    cart_item1 = CartItem(user_id=user_id1, item_id=item_id1, quantity=1)
    cart_item2 = CartItem(user_id=user_id1, item_id=item_id2, quantity=2)
    cart_item3 = CartItem(user_id=user_id2, item_id=item_id1, quantity=3)
    cart_item4 = CartItem(user_id=user_id2, item_id=item_id2, quantity=4)

    await cart_item_repository.save(cart_item1)
    await cart_item_repository.save(cart_item2)
    await cart_item_repository.save(cart_item3)
    await cart_item_repository.save(cart_item4)

    found = await cart_item_repository.find_by_user_and_item(user_id2, item_id1)

    assert found == cart_item3
    assert found.quantity == 3
