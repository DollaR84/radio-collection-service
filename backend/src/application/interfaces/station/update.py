from abc import abstractmethod
from typing import Protocol

from db import domain


class UpdateStationInterface(Protocol):

    @abstractmethod
    async def update_station_status(self, update_data: domain.UpdateStationStatusModel) -> int:
        ...

    @abstractmethod
    async def update_stations_status(self, update_data: list[domain.UpdateStationStatusModel]) -> list[int]:
        ...
