from abc import abstractmethod
from typing import Optional, Protocol

from db import domain


class GetStationInterface(Protocol):

    @abstractmethod
    async def get_station(self, station_id: int) -> Optional[domain.StationModel]:
        ...

    @abstractmethod
    async def get_stations(self) -> list[domain.StationModel]:
        ...

    async def get_stations_urls(self) -> list[str]:
        ...
