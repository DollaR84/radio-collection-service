from sqlalchemy import delete

from ..base import BaseGateway

from ...models import File


class DeleteFileGateway(BaseGateway[int, File]):

    async def delete_file(self, file_id: int) -> None:
        stmt = delete(File)
        stmt = stmt.where(File.id == file_id)

        error_message = f"Error deleting file id={file_id}"
        await self._delete(stmt, error_message)
