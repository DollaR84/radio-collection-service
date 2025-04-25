from application import dto
from application import interfaces

from db import domain


class CreateUser:

    def __init__(self, gateway: interfaces.CreateUserInterface):
        self.gateway = gateway

    async def __call__(
            self,
            data: dto.NewUser,
    ) -> dto.User:
        domain_data = domain.NewUserModel(**data.dict())
        result = await self.gateway.create_user(domain_data)
        return dto.User(**result.dict())
