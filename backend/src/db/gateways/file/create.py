from sqlalchemy import insert

from db import domain

from ..base import BaseGateway

from ...models import File


class CreateFileGateway(BaseGateway[int, File]):

    async def create_file(self, data: domain.NewFileModel) -> int:
        stmt = insert(File).values(**data.dict()).returning(File.id)
        error_message = "Error creating new file"

        return await self._create(stmt, error_message)
