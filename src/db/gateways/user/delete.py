import logging
from typing import Optional
import uuid

from sqlalchemy import delete
from sqlalchemy.exc import SQLAlchemyError

from ..base import BaseGateway

from ...models import User


class DeleteUserGateway(BaseGateway):

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

        try:
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            id_str = f"uuid_id={uuid_id}" if uuid_id else f"id={user_id}"
            raise ValueError(f"Error deleting User {id_str}") from error
