from typing import Optional

from sqlalchemy import select

from application.types import FilePlaylistType

from db import domain

from ..base import BaseGateway

from ...models import File


class GetFileGateway(BaseGateway[int, File]):

    async def get_file_by_id(self, file_id: int) -> Optional[domain.FileModel]:
        error_message = f"Error get file by id='{file_id}'"
        stmt = select(File)
        stmt = stmt.where(File.id == file_id)

        file = await self._get(stmt, error_message)
        return domain.FileModel(**file.dict()) if file else None

    async def get_user_files(self, user_id: int) -> list[domain.FileModel]:
        error_message = f"Error get files for user_id='{user_id}'"
        stmt = select(File)
        stmt = stmt.where(File.user_id == user_id)

        files = await self._get(stmt, error_message, is_multiple=True)
        return [domain.FileModel(**file.dict()) for file in files]

    async def get_files_for_parse(self, file_type: FilePlaylistType) -> list[domain.FileModel]:
        error_message = f"Error get '{file_type.value}' files for parsing"
        stmt = select(File)

        stmt = stmt.where(File.is_load.is_(False))
        stmt = stmt.where(File.fileext == file_type.value)

        files = await self._get(stmt, error_message, is_multiple=True)
        return [domain.FileModel(**file.dict()) for file in files]
