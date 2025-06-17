import uuid

from sqlalchemy import insert

from db import domain

from ..base import BaseGateway

from ...models import AccessPermission, User


class CreateUserGateway(BaseGateway[uuid.UUID, User]):

    async def create_user(
            self,
            data: domain.NewUserModel,
    ) -> uuid.UUID:
        stmt = insert(User).values(**data.dict()).returning(User.uuid_id)
        error_message = "Error creating new user"

        return await self._create(stmt, error_message)


class CreateAccessPermissionGateway(BaseGateway[int, AccessPermission]):

    async def create_permission(self, data: domain.CreateAccessPermissionModel) -> int:
        stmt = insert(AccessPermission).values(**data.dict(exclude_unset=True)).returning(AccessPermission.id)
        error_message = f"Error creating new access permission for user id={data.user_id}"

        return await self._create(stmt, error_message)
