from datetime import datetime, timedelta, timezone
from typing import Optional

from application import dto
from application import interactors
from application.types import UserAccessRights

from config import ResolverConfig


class Resolver:

    def __init__(
            self,
            config: ResolverConfig,
            creator: interactors.CreateAccessPermission,
            getter: interactors.GetAccessPermission,
            getters: interactors.GetAccessPermissions,
            updator: interactors.UpdateAccessPermission,
    ):
        self.config = config
        self.creator = creator
        self.getter = getter
        self.getters = getters
        self.updator = updator

    async def create(self, user_id: int, access_rights: UserAccessRights, reason: Optional[str] = None) -> None:
        time_delta = timedelta(days=getattr(self.config, access_rights.value))
        expires_at = datetime.now(timezone.utc) + time_delta

        permission = dto.CreateAccessPermission(
            user_id=user_id,
            expires_at=expires_at,
            access_rights=access_rights,
            reason=reason,
        )
        await self.creator(permission)

    async def get(
            self,
            user_id: Optional[int] = None,
            access_rights: Optional[UserAccessRights] = None,
    ) -> list[dto.AccessPermission]:
        return await self.getters(user_id, access_rights)

    async def update(
            self,
            permission_id: int,
            added_days: Optional[int] = None,
            access_rights: Optional[UserAccessRights] = None,
    ) -> None:
        update_data = dto.UpdateAccessPermission()
        permission = await self.getter(permission_id)
        if permission is None:
            return

        if added_days:
            expires_at = permission.expires_at + timedelta(days=added_days)
            update_data.expires_at = expires_at

        if access_rights:
            update_data.access_rights = access_rights

        await self.updator(permission_id, update_data)
