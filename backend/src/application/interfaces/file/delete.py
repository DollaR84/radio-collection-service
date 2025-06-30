from abc import abstractmethod
from typing import Protocol


class DeleteFileInterface(Protocol):

    @abstractmethod
    async def delete_file(self, file_id: int) -> None:
        ...
