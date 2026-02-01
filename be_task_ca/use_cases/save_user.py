import hashlib

from be_task_ca.domain.entities.user import User
from be_task_ca.ports.repositories.user_repository import UserRepository
from be_task_ca.use_cases.commands.user_commands import CreateUserCommand
from be_task_ca.use_cases.exceptions.user_exceptions import EmailAlreadyExistsError


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def __call__(self, command: CreateUserCommand) -> User:
        existing_user = await self.user_repository.find_by_email(command.email)
        if existing_user is not None:
            raise EmailAlreadyExistsError(email=command.email)

        hashed_password = hashlib.sha256(command.password.encode()).hexdigest()

        user = User(
            email=command.email,
            first_name=command.first_name,
            last_name=command.last_name,
            hashed_password=hashed_password,
            shipping_address=command.shipping_address or "",
        )

        saved_user = await self.user_repository.save(user)

        return saved_user
