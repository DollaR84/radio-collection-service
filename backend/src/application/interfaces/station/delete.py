from abc import abstractmethod
from typing import Protocol


class DeleteStationInterface(Protocol):

    @abstractmethod
    async def delete_station(
            self,
            station_id: int,
    ) -> None:
        ...
