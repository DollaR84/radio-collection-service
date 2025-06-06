from abc import abstractmethod
from typing import Protocol

from db import domain


class CreateStationInterface(Protocol):

    @abstractmethod
    async def create_station(
            self,
            data: domain.CreateStationModel,
    ) -> int:
        ...

    @abstractmethod
    async def create_stations(
            self,
            data: list[domain.CreateStationModel],
    ) -> list[int]:
        ...


class CreateFavoriteInterface(Protocol):

    @abstractmethod
    async def create_favorite(self, user_id: int, station_id: int) -> int:
        ...
