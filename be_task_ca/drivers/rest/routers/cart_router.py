from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from be_task_ca.use_cases.add_cart_item_to_cart import AddItemToCartUseCase
from be_task_ca.use_cases.get_user_cart import GetUserCartUseCase
from be_task_ca.use_cases.commands.cart_commands import AddToCartCommand
from be_task_ca.drivers.rest.dependencies import (
    get_add_item_to_cart_use_case,
    get_user_cart_use_case,
)
from be_task_ca.drivers.rest.schemas.cart_schemas import (
    AddToCartRequest,
    CartItemResponse,
)

router = APIRouter(
    prefix="/users/{user_id}/cart",
    tags=["cart"],
)


@router.post("/", response_model=CartItemResponse, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    user_id: UUID,
    request: AddToCartRequest,
    use_case: Annotated[AddItemToCartUseCase, Depends(get_add_item_to_cart_use_case)],
) -> CartItemResponse:
    command = AddToCartCommand(
        user_id=user_id,
        item_id=request.item_id,
        quantity=request.quantity,
    )

    cart_item = await use_case(command)

    return CartItemResponse(
        user_id=cart_item.user_id,
        item_id=cart_item.item_id,
        quantity=cart_item.quantity,
    )


@router.get("/", response_model=List[CartItemResponse], status_code=status.HTTP_200_OK)
async def get_cart(
    user_id: UUID,
    use_case: Annotated[GetUserCartUseCase, Depends(get_user_cart_use_case)],
) -> List[CartItemResponse]:
    cart_items = await use_case(user_id)

    return [
        CartItemResponse(
            user_id=cart_item.user_id,
            item_id=cart_item.item_id,
            quantity=cart_item.quantity,
        )
        for cart_item in cart_items
    ]
