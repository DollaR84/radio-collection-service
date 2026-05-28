from typing import Optional

from application import dto
from application import interactors
from application.services import Resolver
from application.types import UserAccessRights

from utils.android import is_valid_android_id

from .exceptions import SubscribeExpired


class SubscribeService:

    def __init__(self, resolver: Resolver, updater: interactors.UpdateUserByUUID):
        self.resolver = resolver
        self.updater = updater

    async def __call__(self, user: dto.User, device_id: Optional[str] = None) -> None:
        if device_id is None or not self._is_valid_device(device_id):
            return

        await self._ensure_subscription(user, device_id)
        is_new_device = user.device_id != device_id

        if is_new_device:
            await self._bind_device(user, device_id)
            await self._create_trial_subscription(user)

    def _is_valid_device(self, device_id: Optional[str] = None) -> bool:
        return bool(device_id and is_valid_android_id(device_id))

    async def _bind_device(self, user: dto.User, device_id: str) -> None:
        update_data = dto.UpdateUser(
            device_id=device_id,
            access_rights=UserAccessRights.PLUS if not user.is_admin else None,
        )

        await self.updater(user.uuid_id, update_data)

    async def _ensure_subscription(self, user: dto.User, device_id: str) -> None:
        if user.device_id and user.device_id == device_id:
            if not user.is_admin and not await self.resolver.get_current_permission(user.id):
                raise SubscribeExpired

    async def _create_trial_subscription(self, user: dto.User) -> None:
        await self.resolver.create(user.id, UserAccessRights.PLUS, days=7, reason="set android test period")
