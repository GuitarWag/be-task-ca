from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from be_task_ca.domain.entities.cart_item import CartItem
from be_task_ca.domain.entities.user import User
from be_task_ca.use_cases.exceptions.user_exceptions import UserNotFoundError
from be_task_ca.use_cases.get_user_cart import GetUserCartUseCase


@pytest.fixture
def cart_item_repository():
    return AsyncMock()


@pytest.fixture
def user_repository():
    return AsyncMock()


@pytest.fixture
def get_user_cart_use_case(cart_item_repository, user_repository):
    return GetUserCartUseCase(cart_item_repository, user_repository)


@pytest.mark.asyncio
async def test_get_user_cart_returns_cart_items(
    get_user_cart_use_case, cart_item_repository, user_repository
):
    user_id = uuid4()

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    cart_item1 = CartItem(user_id=user_id, item_id=uuid4(), quantity=2)
    cart_item2 = CartItem(user_id=user_id, item_id=uuid4(), quantity=1)

    user_repository.find_by_id.return_value = user
    cart_item_repository.find_cart_items_for_user_id.return_value = [
        cart_item1,
        cart_item2,
    ]

    result = await get_user_cart_use_case(user_id)

    assert len(result) == 2
    assert result[0] == cart_item1
    assert result[1] == cart_item2
    user_repository.find_by_id.assert_called_once_with(user_id)
    cart_item_repository.find_cart_items_for_user_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_cart_empty_cart(
    get_user_cart_use_case, cart_item_repository, user_repository
):
    user_id = uuid4()

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    user_repository.find_by_id.return_value = user
    cart_item_repository.find_cart_items_for_user_id.return_value = []

    result = await get_user_cart_use_case(user_id)

    assert result == []
    user_repository.find_by_id.assert_called_once_with(user_id)
    cart_item_repository.find_cart_items_for_user_id.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_get_user_cart_user_not_found(
    get_user_cart_use_case, cart_item_repository, user_repository
):
    user_id = uuid4()

    user_repository.find_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await get_user_cart_use_case(user_id)

    user_repository.find_by_id.assert_called_once_with(user_id)
    cart_item_repository.find_cart_items_for_user_id.assert_not_called()


@pytest.mark.asyncio
async def test_get_user_cart_single_item(
    get_user_cart_use_case, cart_item_repository, user_repository
):
    user_id = uuid4()

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    cart_item = CartItem(user_id=user_id, item_id=uuid4(), quantity=3)

    user_repository.find_by_id.return_value = user
    cart_item_repository.find_cart_items_for_user_id.return_value = [cart_item]

    result = await get_user_cart_use_case(user_id)

    assert len(result) == 1
    assert result[0].quantity == 3


@pytest.mark.asyncio
async def test_get_user_cart_multiple_items(
    get_user_cart_use_case, cart_item_repository, user_repository
):
    user_id = uuid4()

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    items = [
        CartItem(user_id=user_id, item_id=uuid4(), quantity=i) for i in range(1, 6)
    ]

    user_repository.find_by_id.return_value = user
    cart_item_repository.find_cart_items_for_user_id.return_value = items

    result = await get_user_cart_use_case(user_id)

    assert len(result) == 5
    for i, cart_item in enumerate(result):
        assert cart_item.quantity == i + 1


@pytest.mark.asyncio
async def test_get_user_cart_preserves_cart_item_properties(
    get_user_cart_use_case, cart_item_repository, user_repository
):
    user_id = uuid4()
    item_id = uuid4()

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    cart_item = CartItem(user_id=user_id, item_id=item_id, quantity=5)

    user_repository.find_by_id.return_value = user
    cart_item_repository.find_cart_items_for_user_id.return_value = [cart_item]

    result = await get_user_cart_use_case(user_id)

    assert result[0].user_id == user_id
    assert result[0].item_id == item_id
    assert result[0].quantity == 5
