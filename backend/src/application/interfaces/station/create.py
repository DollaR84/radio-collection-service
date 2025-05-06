from abc import abstractmethod
from typing import Protocol

from db import domain


class CreateStationInterface(Protocol):

    @abstractmethod
    async def create_station(
            self,
            data: domain.StationModel,
    ) -> int:
        ...

    @abstractmethod
    async def create_stations(
            self,
            data: list[domain.StationModel],
    ) -> list[int]:
        ...
