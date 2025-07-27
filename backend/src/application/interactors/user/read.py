from typing import Optional
import uuid

from application import dto
from application import interfaces
from application.types import UserAccessRights


class BaseGetUser:

    def __init__(self, gateway: interfaces.GetUserInterface):
        self.gateway = gateway


class GetUserByID(BaseGetUser):

    async def __call__(self, user_id: int) -> Optional[dto.User]:
        domain_data = await self.gateway.get_user_by_id(user_id)
        return dto.User(**domain_data.dict()) if domain_data else None


class GetUserByUUID(BaseGetUser):

    async def __call__(self, uuid_id: uuid.UUID) -> Optional[dto.User]:
        domain_data = await self.gateway.get_user_by_uuid(uuid_id)
        return dto.User(**domain_data.dict()) if domain_data else None


class GetUserByGoogle(BaseGetUser):

    async def __call__(self, google_id: str) -> Optional[dto.User]:
        domain_data = await self.gateway.get_user_by_google(google_id)
        return dto.User(**domain_data.dict()) if domain_data else None


class GetUserByEmail(BaseGetUser):

    async def __call__(self, email: str) -> Optional[dto.User]:
        domain_data = await self.gateway.get_user_by_email(email)
        return dto.User(**domain_data.dict()) if domain_data else None


class BaseGetAccessPermission:

    def __init__(self, gateway: interfaces.GetAccessPermissionInterface):
        self.gateway = gateway


class GetAccessPermission(BaseGetAccessPermission):

    async def __call__(self, permission_id: int) -> Optional[dto.AccessPermission]:
        permission = await self.gateway.get_permission(permission_id)
        return dto.AccessPermission(**permission.dict()) if permission else None


class GetCurrentAccessPermission(BaseGetAccessPermission):

    async def __call__(self, user_id: int) -> Optional[dto.AccessPermission]:
        permission = await self.gateway.get_current_permission(user_id)
        return dto.AccessPermission(**permission.dict()) if permission else None


class GetAccessPermissions(BaseGetAccessPermission):

    async def __call__(
            self,
            user_id: Optional[int] = None,
            access_rights: Optional[UserAccessRights] = None,
    ) -> list[dto.AccessPermission]:
        permissions = await self.gateway.get_permissions(user_id, access_rights)
        return [
            dto.AccessPermission(**permission.dict())
            for permission in permissions
        ]
