import uuid

from application import dto
from application import interfaces

from db import domain


class BaseUpdateUser:

    def __init__(self, gateway: interfaces.UpdateUserInterface):
        self.gateway = gateway


class UpdateUserByID(BaseUpdateUser):

    async def __call__(self, user_id: int, update_data: dto.UpdateUser) -> int:
        domain_data = domain.UpdateUserModel(**update_data.dict())
        return await self.gateway.update_user_by_id(user_id, domain_data)


class UpdateUserByUUID(BaseUpdateUser):

    async def __call__(self, uuid_id: uuid.UUID, update_data: dto.UpdateUser) -> int:
        domain_data = domain.UpdateUserModel(**update_data.dict())
        return await self.gateway.update_user_by_uuid(uuid_id, domain_data)


class UpdateUserByGoogle(BaseUpdateUser):

    async def __call__(self, google_id: str, update_data: dto.UpdateUser) -> int:
        domain_data = domain.UpdateUserModel(**update_data.dict())
        return await self.gateway.update_user_by_google(google_id, domain_data)


class UpdateUserByEmail(BaseUpdateUser):

    async def __call__(self, email: str, update_data: dto.UpdateUser) -> int:
        domain_data = domain.UpdateUserModel(**update_data.dict())
        return await self.gateway.update_user_by_email(email, domain_data)
