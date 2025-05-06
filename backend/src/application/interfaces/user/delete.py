from abc import abstractmethod
from typing import Optional, Protocol
import uuid


class DeleteUserInterface(Protocol):

    @abstractmethod
    async def delete_user(
            self,
            user_id: Optional[int] = None,
            uuid_id: Optional[uuid.UUID] = None,
    ) -> None:
        ...
