from uuid import uuid4
from unittest.mock import AsyncMock

import pytest

from be_task_ca.domain.entities.cart_item import CartItem
from be_task_ca.domain.entities.item import Item
from be_task_ca.domain.entities.user import User
from be_task_ca.use_cases.commands.cart_commands import AddToCartCommand
from be_task_ca.use_cases.exceptions.user_exceptions import UserNotFoundError
from be_task_ca.use_cases.exceptions.item_exceptions import (
    ItemNotFoundError,
    InsufficientStockError,
)
from be_task_ca.use_cases.exceptions.cart_exceptions import ItemAlreadyInCartError
from be_task_ca.use_cases.add_cart_item_to_cart import AddItemToCartUseCase


@pytest.fixture
def cart_item_repository():
    return AsyncMock()


@pytest.fixture
def user_repository():
    return AsyncMock()


@pytest.fixture
def item_repository():
    return AsyncMock()


@pytest.fixture
def add_item_to_cart_use_case(cart_item_repository, user_repository, item_repository):
    return AddItemToCartUseCase(
        cart_item_repository, user_repository, item_repository
    )


@pytest.mark.asyncio
async def test_add_item_to_cart_successfully(
    add_item_to_cart_use_case, cart_item_repository, user_repository, item_repository
):
    user_id = uuid4()
    item_id = uuid4()
    quantity = 2

    command = AddToCartCommand(user_id=user_id, item_id=item_id, quantity=quantity)

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    item = Item(
        id=item_id, name="Item", description="Description", price=10.0, quantity=10
    )

    cart_item = CartItem(user_id=user_id, item_id=item_id, quantity=quantity)

    user_repository.find_by_id.return_value = user
    item_repository.find_by_id.return_value = item
    cart_item_repository.find_by_user_and_item.return_value = None
    cart_item_repository.save.return_value = cart_item

    result = await add_item_to_cart_use_case(command)

    assert result.user_id == user_id
    assert result.item_id == item_id
    assert result.quantity == quantity
    user_repository.find_by_id.assert_called_once_with(user_id)
    item_repository.find_by_id.assert_called_once_with(item_id)
    cart_item_repository.find_by_user_and_item.assert_called_once_with(
        user_id, item_id
    )
    cart_item_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_add_item_to_cart_user_not_found(
    add_item_to_cart_use_case, cart_item_repository, user_repository, item_repository
):
    user_id = uuid4()
    item_id = uuid4()

    command = AddToCartCommand(user_id=user_id, item_id=item_id, quantity=1)

    user_repository.find_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await add_item_to_cart_use_case(command)

    user_repository.find_by_id.assert_called_once_with(user_id)
    item_repository.find_by_id.assert_not_called()
    cart_item_repository.find_by_user_and_item.assert_not_called()
    cart_item_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_item_to_cart_item_not_found(
    add_item_to_cart_use_case, cart_item_repository, user_repository, item_repository
):
    user_id = uuid4()
    item_id = uuid4()

    command = AddToCartCommand(user_id=user_id, item_id=item_id, quantity=1)

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    user_repository.find_by_id.return_value = user
    item_repository.find_by_id.return_value = None

    with pytest.raises(ItemNotFoundError):
        await add_item_to_cart_use_case(command)

    user_repository.find_by_id.assert_called_once_with(user_id)
    item_repository.find_by_id.assert_called_once_with(item_id)
    cart_item_repository.find_by_user_and_item.assert_not_called()
    cart_item_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_item_to_cart_insufficient_stock(
    add_item_to_cart_use_case, cart_item_repository, user_repository, item_repository
):
    user_id = uuid4()
    item_id = uuid4()

    command = AddToCartCommand(user_id=user_id, item_id=item_id, quantity=10)

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    item = Item(
        id=item_id, name="Item", description="Description", price=10.0, quantity=5
    )

    user_repository.find_by_id.return_value = user
    item_repository.find_by_id.return_value = item

    with pytest.raises(InsufficientStockError):
        await add_item_to_cart_use_case(command)

    user_repository.find_by_id.assert_called_once_with(user_id)
    item_repository.find_by_id.assert_called_once_with(item_id)
    cart_item_repository.find_by_user_and_item.assert_not_called()
    cart_item_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_item_to_cart_item_already_in_cart(
    add_item_to_cart_use_case, cart_item_repository, user_repository, item_repository
):
    user_id = uuid4()
    item_id = uuid4()

    command = AddToCartCommand(user_id=user_id, item_id=item_id, quantity=1)

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    item = Item(
        id=item_id, name="Item", description="Description", price=10.0, quantity=10
    )

    existing_cart_item = CartItem(user_id=user_id, item_id=item_id, quantity=1)

    user_repository.find_by_id.return_value = user
    item_repository.find_by_id.return_value = item
    cart_item_repository.find_by_user_and_item.return_value = existing_cart_item

    with pytest.raises(ItemAlreadyInCartError):
        await add_item_to_cart_use_case(command)

    user_repository.find_by_id.assert_called_once_with(user_id)
    item_repository.find_by_id.assert_called_once_with(item_id)
    cart_item_repository.find_by_user_and_item.assert_called_once_with(
        user_id, item_id
    )
    cart_item_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_add_item_to_cart_exact_stock_available(
    add_item_to_cart_use_case, cart_item_repository, user_repository, item_repository
):
    user_id = uuid4()
    item_id = uuid4()
    quantity = 5

    command = AddToCartCommand(user_id=user_id, item_id=item_id, quantity=quantity)

    user = User(
        id=user_id,
        email="test@example.com",
        first_name="Test",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    item = Item(
        id=item_id,
        name="Item",
        description="Description",
        price=10.0,
        quantity=quantity,
    )

    cart_item = CartItem(user_id=user_id, item_id=item_id, quantity=quantity)

    user_repository.find_by_id.return_value = user
    item_repository.find_by_id.return_value = item
    cart_item_repository.find_by_user_and_item.return_value = None
    cart_item_repository.save.return_value = cart_item

    result = await add_item_to_cart_use_case(command)

    assert result.quantity == quantity
    cart_item_repository.save.assert_called_once()
