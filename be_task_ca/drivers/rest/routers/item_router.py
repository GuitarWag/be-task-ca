from typing import Annotated, List

from fastapi import APIRouter, Depends, status

from be_task_ca.use_cases.create_item import CreateItemUseCase
from be_task_ca.use_cases.get_all_items import GetAllItemsUseCase
from be_task_ca.use_cases.commands.item_commands import CreateItemCommand
from be_task_ca.drivers.rest.dependencies import (
    get_create_item_use_case,
    get_all_items_use_case,
)
from be_task_ca.drivers.rest.schemas.item_schemas import CreateItemRequest, ItemResponse

router = APIRouter(
    prefix="/items",
    tags=["items"],
)


@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    request: CreateItemRequest,
    use_case: Annotated[CreateItemUseCase, Depends(get_create_item_use_case)],
) -> ItemResponse:
    command = CreateItemCommand(
        name=request.name,
        description=request.description,
        price=request.price,
        quantity=request.quantity,
    )

    item = await use_case(command)

    return ItemResponse(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        quantity=item.quantity,
    )


@router.get("/", response_model=List[ItemResponse], status_code=status.HTTP_200_OK)
async def get_all_items(
    use_case: Annotated[GetAllItemsUseCase, Depends(get_all_items_use_case)],
) -> List[ItemResponse]:
    items = await use_case()

    return [
        ItemResponse(
            id=item.id,
            name=item.name,
            description=item.description,
            price=item.price,
            quantity=item.quantity,
        )
        for item in items
    ]
