import uuid

from sqlalchemy import insert

from db import domain

from ..base import BaseGateway

from ...models import User


class CreateUserGateway(BaseGateway[uuid.UUID, User]):

    async def create_user(
            self,
            data: domain.NewUserModel,
    ) -> uuid.UUID:
        stmt = insert(User).values(**data.dict()).returning(User.uuid_id)
        error_message = "Error creating new user"

        return await self._create(stmt, error_message)
