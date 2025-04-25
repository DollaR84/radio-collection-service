from typing import Optional
import uuid

from application import interfaces


class DeleteUser:

    def __init__(self, gateway: interfaces.DeleteUserInterface):
        self.gateway = gateway

    async def __call__(
            self,
            user_id: Optional[int] = None,
            uuid_id: Optional[uuid.UUID] = None,
    ) -> None:
        await self.gateway.delete_user(user_id, uuid_id)
