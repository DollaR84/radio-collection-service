from application import interfaces


class DeleteFile:

    def __init__(self, gateway: interfaces.DeleteFileInterface):
        self.gateway = gateway

    async def __call__(self, file_id: int) -> None:
        await self.gateway.delete_file(file_id)
