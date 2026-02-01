from uuid import UUID


class EmailAlreadyExistsError(Exception):
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"Email {email} already exists")


class UserNotFoundError(Exception):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")
