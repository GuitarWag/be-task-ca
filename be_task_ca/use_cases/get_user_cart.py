from typing import List
from uuid import UUID

from be_task_ca.domain.entities.cart_item import CartItem
from be_task_ca.ports.repositories.cart_item_repository import CartItemRepository
from be_task_ca.ports.repositories.user_repository import UserRepository
from be_task_ca.use_cases.exceptions.user_exceptions import UserNotFoundError


class GetUserCartUseCase:
    def __init__(
        self,
        cart_item_repository: CartItemRepository,
        user_repository: UserRepository,
    ):
        self.cart_item_repository = cart_item_repository
        self.user_repository = user_repository

    async def __call__(self, user_id: UUID) -> List[CartItem]:
        user = await self.user_repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundError(user_id=user_id)

        cart_items = await self.cart_item_repository.find_cart_items_for_user_id(
            user_id
        )

        return cart_items
