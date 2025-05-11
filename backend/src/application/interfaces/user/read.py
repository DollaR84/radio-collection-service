from abc import abstractmethod
from typing import Protocol, Optional
import uuid

from db import domain


class GetUserInterface(Protocol):

    @abstractmethod
    async def get_user_by_id(self, user_id: int) -> Optional[domain.UserModel]:
        ...

    @abstractmethod
    async def get_user_by_uuid(self, uuid_id: uuid.UUID) -> Optional[domain.UserModel]:
        ...

    @abstractmethod
    async def get_user_by_google(self, google_id: str) -> Optional[domain.UserModel]:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: str) -> Optional[domain.UserModel]:
        ...
