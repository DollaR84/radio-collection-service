from abc import abstractmethod
from typing import Protocol
import uuid

from db import domain


class CreateUserInterface(Protocol):

    @abstractmethod
    async def create_user(
            self,
            data: domain.NewUserModel,
    ) -> uuid.UUID:
        ...


class CreateAccessPermissionInterface(Protocol):

    @abstractmethod
    async def create_permission(self, data: domain.CreateAccessPermissionModel) -> int:
        ...
