from datetime import datetime
from typing import Optional
import uuid

from application.types import UserAccessRights

from sqlalchemy import select
from sqlalchemy.sql import Select

from db import domain

from ..base import BaseGateway

from ...models import AccessPermission, User


class GetUserGateway(BaseGateway[int, User]):

    async def get_user_by_id(self, user_id: int) -> Optional[domain.UserModel]:
        error_message = f"Error get user by id='{user_id}'"
        stmt = select(User)
        stmt = stmt.where(User.id == user_id)
        return await self._get_user(stmt, error_message)

    async def get_user_by_uuid(self, uuid_id: uuid.UUID) -> Optional[domain.UserModel]:
        error_message = f"Error get user by uuid='{uuid_id}'"
        stmt = select(User)
        stmt = stmt.where(User.uuid_id == uuid_id)
        return await self._get_user(stmt, error_message)

    async def get_user_by_google(self, google_id: str) -> Optional[domain.UserModel]:
        error_message = f"Error get user by google_id='{google_id}'"
        stmt = select(User)
        stmt = stmt.where(User.google_id == google_id)
        return await self._get_user(stmt, error_message)

    async def get_user_by_email(self, email: str) -> Optional[domain.UserModel]:
        error_message = f"Error get user by email='{email}'"
        stmt = select(User)
        stmt = stmt.where(User.email == email)
        return await self._get_user(stmt, error_message)

    async def _get_user(self, stmt: Select, error_message: str) -> Optional[domain.UserModel]:
        user = await self._get(stmt, error_message)
        if user:
            return domain.UserModel(**user.dict())
        return None

    async def get_users(
            self,
            exclude_access_rights: Optional[list[UserAccessRights]] = None,
    ) -> list[domain.UserModel]:
        error_message = "Error get users"
        stmt = select(User)

        if exclude_access_rights:
            stmt = stmt.where(User.access_rights.not_in(exclude_access_rights))

        users = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.UserModel(**user.dict())
            for user in users
        ]


class GetAccessPermissionGateway(BaseGateway[int, AccessPermission]):

    async def get_permission(self, permission_id: int) -> Optional[domain.AccessPermissionModel]:
        error_message = f"Error get user permission id={permission_id}"
        stmt = select(AccessPermission)
        stmt = stmt.where(AccessPermission.id == permission_id)

        permission = await self._get(stmt, error_message)
        return domain.AccessPermissionModel(**permission.dict()) if permission else None

    async def get_current_permission(self, user_id: int) -> Optional[domain.AccessPermissionModel]:
        error_message = f"Error get user current permission for user_id={user_id}"
        stmt = select(AccessPermission)
        stmt = stmt.where(AccessPermission.user_id == user_id)
        stmt = stmt.where(AccessPermission.expires_at > datetime.utcnow())

        permission = await self._get(stmt, error_message)
        return domain.AccessPermissionModel(**permission.dict()) if permission else None

    async def get_permissions(
            self,
            user_id: Optional[int] = None,
            access_rights: Optional[UserAccessRights] = None,
    ) -> list[domain.AccessPermissionModel]:
        error_message = "Error get user permissions"
        stmt = select(AccessPermission)

        if user_id:
            stmt = stmt.where(AccessPermission.user_id == user_id)

        if access_rights:
            stmt = stmt.where(AccessPermission.access_rights == access_rights)
        stmt = stmt.order_by(AccessPermission.id)

        permissions = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.AccessPermissionModel(**permission.dict())
            for permission in permissions
        ]
