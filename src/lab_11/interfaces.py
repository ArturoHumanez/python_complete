from typing import Optional, Protocol

from src.lab_8.models import User


class UserRepository(Protocol):
    def get_by_id(self, user_id: int) -> Optional[User]:
        ...

    def save(self, user: User) -> None:
        ...
