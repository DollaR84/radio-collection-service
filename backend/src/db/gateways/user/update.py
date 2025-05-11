import uuid

from sqlalchemy import update
from sqlalchemy.sql import Update

from db import domain

from ..base import BaseGateway

from ...models import User


class UpdateUserGateway(BaseGateway[int, User]):

    async def update_user_by_id(self, user_id: int, update_data: domain.UpdateUserModel) -> int:
        error_message = "Error update user by id='{user_id}'"
        stmt = update(User)
        stmt = stmt.where(User.id == user_id)

        return await self._update_user(stmt, update_data, error_message)

    async def update_user_by_uuid(self, uuid_id: uuid.UUID, update_data: domain.UpdateUserModel) -> int:
        error_message = "Error update user by uuid='{uuid_id}'"
        stmt = update(User)
        stmt = stmt.where(User.uuid_id == uuid_id)

        return await self._update_user(stmt, update_data, error_message)

    async def update_user_by_google(self, google_id: str, update_data: domain.UpdateUserModel) -> int:
        error_message = "Error update user by google_id='{google_id}'"
        stmt = update(User)
        stmt = stmt.where(User.google_id == google_id)

        return await self._update_user(stmt, update_data, error_message)

    async def update_user_by_email(self, email: str, update_data: domain.UpdateUserModel) -> int:
        error_message = "Error update user by email='{email}'"
        stmt = update(User)
        stmt = stmt.where(User.email == email)

        return await self._update_user(stmt, update_data, error_message)

    async def _update_user(self, stmt: Update, update_data: domain.UpdateUserModel, error_message: str) -> int:
        stmt = stmt.values(**update_data.dict(exclude_unset=True))
        stmt = stmt.returning(User.id)

        return await self._update(stmt, error_message)
