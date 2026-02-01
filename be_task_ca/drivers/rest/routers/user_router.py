from typing import Annotated

from fastapi import APIRouter, Depends, status

from be_task_ca.use_cases.save_user import CreateUserUseCase
from be_task_ca.use_cases.commands.user_commands import CreateUserCommand
from be_task_ca.drivers.rest.dependencies import get_create_user_use_case
from be_task_ca.drivers.rest.schemas.user_schemas import CreateUserRequest, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    use_case: Annotated[CreateUserUseCase, Depends(get_create_user_use_case)],
) -> UserResponse:
    command = CreateUserCommand(
        email=request.email,
        first_name=request.first_name,
        last_name=request.last_name,
        password=request.password,
        shipping_address=request.shipping_address,
    )

    user = await use_case(command)

    return UserResponse(
        id=user.id,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        shipping_address=user.shipping_address,
    )
