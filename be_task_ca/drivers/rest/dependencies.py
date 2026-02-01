from typing import Annotated
from functools import lru_cache

from fastapi import Depends

from be_task_ca.adapters.repositories.user.in_memory_user_repository import (
    InMemoryUserRepository,
)
from be_task_ca.adapters.repositories.item.in_memory_item_repository import (
    InMemoryItemRepository,
)
from be_task_ca.adapters.repositories.cart_item.in_memory_cart_item_repository import (
    InMemoryCartItemRepository,
)
from be_task_ca.ports.repositories.user_repository import UserRepository
from be_task_ca.ports.repositories.item_repository import ItemRepository
from be_task_ca.ports.repositories.cart_item_repository import CartItemRepository
from be_task_ca.use_cases.save_user import CreateUserUseCase
from be_task_ca.use_cases.create_item import CreateItemUseCase
from be_task_ca.use_cases.get_all_items import GetAllItemsUseCase
from be_task_ca.use_cases.add_cart_item_to_cart import AddItemToCartUseCase
from be_task_ca.use_cases.get_user_cart import GetUserCartUseCase


@lru_cache
def get_user_repository() -> UserRepository:
    return InMemoryUserRepository()


@lru_cache
def get_item_repository() -> ItemRepository:
    return InMemoryItemRepository()


@lru_cache
def get_cart_item_repository() -> CartItemRepository:
    return InMemoryCartItemRepository()


def get_create_user_use_case(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> CreateUserUseCase:
    return CreateUserUseCase(user_repo)


def get_create_item_use_case(
    item_repo: Annotated[ItemRepository, Depends(get_item_repository)],
) -> CreateItemUseCase:
    return CreateItemUseCase(item_repo)


def get_all_items_use_case(
    item_repo: Annotated[ItemRepository, Depends(get_item_repository)],
) -> GetAllItemsUseCase:
    return GetAllItemsUseCase(item_repo)


def get_add_item_to_cart_use_case(
    cart_repo: Annotated[CartItemRepository, Depends(get_cart_item_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
    item_repo: Annotated[ItemRepository, Depends(get_item_repository)],
) -> AddItemToCartUseCase:
    return AddItemToCartUseCase(cart_repo, user_repo, item_repo)


def get_user_cart_use_case(
    cart_repo: Annotated[CartItemRepository, Depends(get_cart_item_repository)],
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> GetUserCartUseCase:
    return GetUserCartUseCase(cart_repo, user_repo)
