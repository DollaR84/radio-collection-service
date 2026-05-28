from typing import Any

from application import dto
from application import interactors

from ... import schemas


class GoogleService:

    def __init__(self, updater: interactors.UpdateUserByUUID):
        self.updater = updater

    def build_user_schema(self, data: dict[str, Any]) -> schemas.UserGoogle:
        return schemas.UserGoogle(
            email=data.get("email"),
            google_id=data.get("sub") or data.get("id"),
            first_name=data.get("given_name"),
            last_name=data.get("family_name"),
            device_id=data.get("device_id"),
        )

    async def __call__(self, user: dto.User, data: schemas.UserGoogle) -> None:
        await self._update_profile(user, data)

    async def _update_profile(self, user: dto.User, data: schemas.UserGoogle) -> None:
        if data.first_name != user.first_name or data.last_name != user.last_name:
            update_data = dto.UpdateUser(first_name=data.first_name, last_name=data.last_name)
            await self.updater(user.uuid_id, update_data)
