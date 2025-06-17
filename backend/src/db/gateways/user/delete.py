from typing import Optional
import uuid

from sqlalchemy import delete

from ..base import BaseGateway

from ...models import AccessPermission, User


class DeleteUserGateway(BaseGateway[int, User]):

    async def delete_user(
            self,
            user_id: Optional[int] = None,
            uuid_id: Optional[uuid.UUID] = None,
    ) -> None:
        if not user_id or not uuid_id:
            raise ValueError("one of the identifiers must be indicated: 'user_id' or 'uuid_id'")

        stmt = delete(User)
        if uuid_id:
            stmt = stmt.where(User.uuid_id == uuid_id)
        else:
            stmt = stmt.where(User.id == user_id)

        id_str = f"uuid_id={uuid_id}" if uuid_id else f"id={user_id}"
        error_message = f"Error deleting User {id_str}"
        await self._delete(stmt, error_message)


class DeleteAccessPermissionGateway(BaseGateway[int, AccessPermission]):

    async def delete_permission(self, permission_id: int) -> None:
        stmt = delete(AccessPermission)
        stmt = stmt.where(AccessPermission.id == permission_id)

        error_message = f"Error deleting access permission with id={permission_id} for user"
        await self._delete(stmt, error_message)
