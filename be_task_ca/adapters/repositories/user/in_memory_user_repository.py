from typing import List, Optional
from uuid import UUID

from be_task_ca.domain.entities.user import User
from be_task_ca.ports.repositories.user_repository import UserRepository


class InMemoryUserRepository(UserRepository):
    users: List[User]

    def __init__(self):
        self.users = []

    async def save(self, user: User) -> User:
        self.users.append(user)
        return user

    async def find_by_email(self, email: str) -> Optional[User]:
        for user in self.users:
            if user.email.lower() == email.lower():
                return user
        return None

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        for user in self.users:
            if user.id == user_id:
                return user
        return None
