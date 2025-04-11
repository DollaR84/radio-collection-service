from abc import abstractmethod
from typing import Protocol

from db import domain


class CreateUser(Protocol):

    @abstractmethod
    async def create_user(
            self,
            data: domain.NewUserModel,
    ) -> domain.UserModel:
        ...
