from abc import abstractmethod
from typing import Protocol
import uuid

from db import domain


class UpdateUserInterface(Protocol):

    @abstractmethod
    async def update_user_by_id(self, user_id: int, update_data: domain.UpdateUserModel) -> int:
        ...

    @abstractmethod
    async def update_user_by_uuid(self, uuid_id: uuid.UUID, update_data: domain.UpdateUserModel) -> int:
        ...

    @abstractmethod
    async def update_user_by_google(self, google_id: str, update_data: domain.UpdateUserModel) -> int:
        ...

    @abstractmethod
    async def update_user_by_email(self, email: str, update_data: domain.UpdateUserModel) -> int:
        ...
