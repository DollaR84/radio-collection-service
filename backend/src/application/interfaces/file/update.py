from abc import abstractmethod
from typing import Protocol

from db import domain


class UpdateFileInterface(Protocol):

    @abstractmethod
    async def update_file(self, file_id: int, update_data: domain.UpdateFileModel) -> int:
        ...
