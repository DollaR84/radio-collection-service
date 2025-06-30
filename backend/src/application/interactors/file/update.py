from application import interfaces

from db import domain


class UpdateFileLoadStatus:

    def __init__(self, gateway: interfaces.UpdateFileInterface):
        self.gateway = gateway

    async def __call__(self, file_id: int) -> int:
        domain_data = domain.UpdateFileModel(is_load=True)
        return await self.gateway.update_file(file_id, domain_data)
