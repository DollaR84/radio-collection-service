import logging

from sqlalchemy.exc import SQLAlchemyError

from db import domain

from ..base import BaseGateway

from ...models import User


class CreateUserGateway(BaseGateway):

    async def create_user(
            self,
            data: domain.NewUserModel,
    ) -> domain.UserModel:
        new_user = User(**data.dict())

        try:
            self.session.add(new_user)
            await self.session.commit()

            return domain.UserModel(uuid_id=new_user.uuid_id)
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError("Error creating new user") from error
