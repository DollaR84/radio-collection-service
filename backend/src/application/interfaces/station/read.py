from abc import abstractmethod
from typing import Optional, Protocol

from application.types import StationStatusType

from db import domain


class GetStationInterface(Protocol):

    @abstractmethod
    async def get_station(self, station_id: int) -> Optional[domain.StationModel]:
        ...

    @abstractmethod
    async def get_stations(
            self,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.StationModel]:
        ...

    @abstractmethod
    async def get_count(
            self,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
    ) -> int:
        ...

    async def get_double_name(self) -> list[domain.StationModel]:
        ...


class GetStationsUrlsInterface(Protocol):

    @abstractmethod
    async def get_stations_urls(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[str]:
        ...

    @abstractmethod
    async def check_station_url(self, url: str) -> bool:
        ...


class GetFavoriteInterface(Protocol):

    @abstractmethod
    async def get_favorites(
            self,
            user_id: int,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.StationModel]:
        ...

    @abstractmethod
    async def get_count(
            self,
            user_id: int,
    ) -> int:
        ...
