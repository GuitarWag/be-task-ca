from be_task_ca.domain.entities.cart_item import CartItem
from be_task_ca.ports.repositories.cart_item_repository import CartItemRepository
from be_task_ca.ports.repositories.item_repository import ItemRepository
from be_task_ca.ports.repositories.user_repository import UserRepository
from be_task_ca.use_cases.commands.cart_commands import AddToCartCommand
from be_task_ca.use_cases.exceptions.user_exceptions import UserNotFoundError
from be_task_ca.use_cases.exceptions.item_exceptions import (
    ItemNotFoundError,
    InsufficientStockError,
)
from be_task_ca.use_cases.exceptions.cart_exceptions import ItemAlreadyInCartError


class AddItemToCartUseCase:
    def __init__(
        self,
        cart_item_repository: CartItemRepository,
        user_repository: UserRepository,
        item_repository: ItemRepository,
    ):
        self.cart_item_repository = cart_item_repository
        self.user_repository = user_repository
        self.item_repository = item_repository

    async def __call__(self, command: AddToCartCommand) -> CartItem:
        user = await self.user_repository.find_by_id(command.user_id)
        if user is None:
            raise UserNotFoundError(user_id=command.user_id)

        item = await self.item_repository.find_by_id(command.item_id)
        if item is None:
            raise ItemNotFoundError(item_id=command.item_id)

        if item.quantity < command.quantity:
            raise InsufficientStockError(
                item_id=command.item_id,
                requested=command.quantity,
                available=item.quantity,
            )

        existing = await self.cart_item_repository.find_by_user_and_item(
            command.user_id, command.item_id
        )
        if existing:
            raise ItemAlreadyInCartError(
                user_id=command.user_id, item_id=command.item_id
            )

        cart_item = CartItem(
            user_id=command.user_id,
            item_id=command.item_id,
            quantity=command.quantity,
        )

        saved_cart_item = await self.cart_item_repository.save(cart_item)

        return saved_cart_item
