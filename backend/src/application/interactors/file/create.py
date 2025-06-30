from application import dto
from application import interfaces

from db import domain


class CreateFile:

    def __init__(self, gateway: interfaces.CreateFileInterface):
        self.gateway = gateway

    async def __call__(self, data: dto.NewFile) -> int:
        domain_data = domain.NewFileModel(**data.dict())
        return await self.gateway.create_file(domain_data)
