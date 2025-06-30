from abc import abstractmethod
from typing import Protocol

from db import domain


class CreateFileInterface(Protocol):

    @abstractmethod
    async def create_file(self, data: domain.NewFileModel) -> int:
        ...
