import hashlib
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock

import pytest

from be_task_ca.domain.entities.user import User
from be_task_ca.use_cases.commands.user_commands import CreateUserCommand
from be_task_ca.use_cases.exceptions.user_exceptions import EmailAlreadyExistsError
from be_task_ca.use_cases.save_user import CreateUserUseCase


@pytest.fixture
def user_repository():
    return AsyncMock()


@pytest.fixture
def create_user_use_case(user_repository):
    return CreateUserUseCase(user_repository)


@pytest.mark.asyncio
async def test_create_user_successfully(create_user_use_case, user_repository):
    command = CreateUserCommand(
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        password="password123",
        shipping_address="123 Main St",
    )

    user = User(
        id=uuid4(),
        email=command.email,
        first_name=command.first_name,
        last_name=command.last_name,
        hashed_password=hashlib.sha256(command.password.encode()).hexdigest(),
        shipping_address=command.shipping_address or "",
    )

    user_repository.find_by_email.return_value = None
    user_repository.save.return_value = user

    result = await create_user_use_case(command)

    assert result.email == "john@example.com"
    assert result.first_name == "John"
    assert result.last_name == "Doe"
    user_repository.find_by_email.assert_called_once_with("john@example.com")
    user_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_with_no_shipping_address(create_user_use_case, user_repository):
    command = CreateUserCommand(
        email="jane@example.com",
        first_name="Jane",
        last_name="Doe",
        password="password123",
        shipping_address=None,
    )

    user = User(
        id=uuid4(),
        email=command.email,
        first_name=command.first_name,
        last_name=command.last_name,
        hashed_password=hashlib.sha256(command.password.encode()).hexdigest(),
        shipping_address="",
    )

    user_repository.find_by_email.return_value = None
    user_repository.save.return_value = user

    result = await create_user_use_case(command)

    assert result.shipping_address == ""
    user_repository.save.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_email_already_exists(create_user_use_case, user_repository):
    command = CreateUserCommand(
        email="existing@example.com",
        first_name="John",
        last_name="Doe",
        password="password123",
    )

    existing_user = User(
        id=uuid4(),
        email="existing@example.com",
        first_name="Existing",
        last_name="User",
        hashed_password="hashed",
        shipping_address="",
    )

    user_repository.find_by_email.return_value = existing_user

    with pytest.raises(EmailAlreadyExistsError):
        await create_user_use_case(command)

    user_repository.find_by_email.assert_called_once_with("existing@example.com")
    user_repository.save.assert_not_called()


@pytest.mark.asyncio
async def test_create_user_hashes_password(create_user_use_case, user_repository):
    command = CreateUserCommand(
        email="test@example.com",
        first_name="Test",
        last_name="User",
        password="mysecretpassword",
    )

    expected_hash = hashlib.sha256("mysecretpassword".encode()).hexdigest()

    user_repository.find_by_email.return_value = None

    saved_user = None

    def capture_saved_user(user):
        nonlocal saved_user
        saved_user = user
        return user

    user_repository.save.side_effect = capture_saved_user

    await create_user_use_case(command)

    assert saved_user.hashed_password == expected_hash
