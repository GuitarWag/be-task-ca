from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserCommand:
    email: str
    first_name: str
    last_name: str
    password: str
    shipping_address: str | None = None
