from typing import Optional

from application import dto
from application import interfaces
from application.types import FilePlaylistType


class BaseGetFile:

    def __init__(self, gateway: interfaces.GetFileInterface):
        self.gateway = gateway


class GetFileByID(BaseGetFile):

    async def __call__(self, file_id: int) -> Optional[dto.File]:
        domain_data = await self.gateway.get_file_by_id(file_id)
        return dto.File(**domain_data.dict()) if domain_data else None


class GetUserFiles(BaseGetFile):

    async def __call__(self, user_id: int) -> list[dto.File]:
        domain_data = await self.gateway.get_user_files(user_id)
        return [dto.File(**file.dict()) for file in domain_data]


class GetM3uFilesForParse(BaseGetFile):

    async def __call__(self) -> list[dto.File]:
        domain_data = await self.gateway.get_files_for_parse(FilePlaylistType.M3U)
        return [dto.File(**file.dict()) for file in domain_data]


class GetPlsFilesForParse(BaseGetFile):

    async def __call__(self) -> list[dto.File]:
        domain_data = await self.gateway.get_files_for_parse(FilePlaylistType.PLS)
        return [dto.File(**file.dict()) for file in domain_data]


class GetJsonFilesForParse(BaseGetFile):

    async def __call__(self) -> list[dto.File]:
        domain_data = await self.gateway.get_files_for_parse(FilePlaylistType.JSON)
        return [dto.File(**file.dict()) for file in domain_data]
