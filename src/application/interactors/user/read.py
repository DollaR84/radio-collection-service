from typing import Optional
import uuid

from application import dto
from application import interfaces


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
