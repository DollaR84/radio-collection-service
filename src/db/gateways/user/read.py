from typing import Optional
import uuid

from sqlalchemy import select
from sqlalchemy.sql import Select

from db import domain

from ..base import BaseGateway

from ...models import User


class GetUserGateway(BaseGateway[int, User]):

    async def get_user_by_id(self, user_id: int) -> Optional[domain.UserModel]:
        error_message = "Error get user by id='{user_id}'"
        stmt = select(User)
        stmt = stmt.where(User.id == user_id)
        return await self._get_user(stmt, error_message)

    async def get_user_by_uuid(self, uuid_id: uuid.UUID) -> Optional[domain.UserModel]:
        error_message = "Error get user by uuid='{uuid_id}'"
        stmt = select(User)
        stmt = stmt.where(User.uuid_id == uuid_id)
        return await self._get_user(stmt, error_message)

    async def get_user_by_google(self, google_id: str) -> Optional[domain.UserModel]:
        error_message = "Error get user by google_id='{google_id}'"
        stmt = select(User)
        stmt = stmt.where(User.google_id == google_id)
        return await self._get_user(stmt, error_message)

    async def get_user_by_email(self, email: str) -> Optional[domain.UserModel]:
        error_message = "Error get user by email='{email}'"
        stmt = select(User)
        stmt = stmt.where(User.email == email)
        return await self._get_user(stmt, error_message)

    async def _get_user(self, stmt: Select, error_message: str) -> Optional[domain.UserModel]:
        user = await self._get(stmt, error_message)
        if user:
            return domain.UserModel(**user.dict(exclude=["created_at", "updated_at"]))
        return None
