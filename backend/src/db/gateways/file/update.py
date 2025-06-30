from sqlalchemy import update

from db import domain

from ..base import BaseGateway

from ...models import File


class UpdateFileGateway(BaseGateway[int, File]):

    async def update_file(self, file_id: int, update_data: domain.UpdateFileModel) -> int:
        error_message = f"Error update file by id='{file_id}'"
        stmt = update(File)
        stmt = stmt.where(File.id == file_id)

        stmt = stmt.values(**update_data.dict(exclude_unset=True))
        stmt = stmt.returning(File.id)

        return await self._update(stmt, error_message)
