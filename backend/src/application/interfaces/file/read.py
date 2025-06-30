from abc import abstractmethod
from typing import Optional, Protocol

from application.types import FilePlaylistType

from db import domain


class GetFileInterface(Protocol):

    @abstractmethod
    async def get_file_by_id(self, file_id: int) -> Optional[domain.FileModel]:
        ...

    async def get_user_files(self, user_id: int) -> list[domain.FileModel]:
        ...

    async def get_files_for_parse(self, file_type: FilePlaylistType) -> list[domain.FileModel]:
        ...
