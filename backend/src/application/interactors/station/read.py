from typing import Optional

from application import dto
from application import interfaces
from application.types import StationStatusType


class BaseGetStation:

    def __init__(self, gateway: interfaces.GetStationInterface):
        self.gateway = gateway


class GetStation(BaseGetStation):

    async def __call__(self, station_id: int) -> Optional[dto.StationData]:
        station = await self.gateway.get_station(station_id)
        return dto.StationData(**station.dict()) if station else None


class GetStations(BaseGetStation):

    async def __call__(
            self,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[dto.StationData]:
        stations = await self.gateway.get_stations(name, info, status, offset, limit)
        return [
            dto.StationData(**station.dict())
            for station in stations
        ]


class GetStationsWithCount(BaseGetStation):

    async def __call__(
            self,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> dto.StationsWithCount:
        count = await self.gateway.get_count(name, info, status)
        stations = await self.gateway.get_stations(name, info, status, offset, limit)

        return dto.StationsWithCount(
            [
                dto.StationData(**station.dict())
                for station in stations
            ],
            count,
        )


class GetStationsWithDoubleName(BaseGetStation):

    async def __call__(self) -> list[dto.StationData]:
        stations = await self.gateway.get_double_name()
        return [
            dto.StationData(**station.dict())
            for station in stations
        ]


class BaseStationUrls:

    def __init__(self, gateway: interfaces.GetStationsUrlsInterface):
        self.gateway = gateway


class GetStationUrls(BaseStationUrls):

    async def __call__(self, offset: Optional[int] = None, limit: Optional[int] = None) -> list[str]:
        return await self.gateway.get_stations_urls(offset=offset, limit=limit)


class CheckStationUrl(BaseStationUrls):

    async def __call__(self, url: str) -> bool:
        return await self.gateway.check_station_url(url)


class BaseUserFavorites:

    def __init__(self, gateway: interfaces.GetFavoriteInterface):
        self.gateway = gateway


class GetUserFavorites(BaseUserFavorites):

    async def __call__(
            self,
            user_id: int,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[dto.StationData]:
        stations = await self.gateway.get_favorites(user_id, offset, limit)
        return [
            dto.StationData(**station.dict())
            for station in stations
        ]


class GetUserFavoritesWithCount(BaseUserFavorites):

    async def __call__(
            self,
            user_id: int,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> dto.StationsWithCount:
        count = await self.gateway.get_count(user_id)
        stations = await self.gateway.get_favorites(user_id, offset, limit)

        return dto.StationsWithCount(
            [
                dto.StationData(**station.dict())
                for station in stations
            ],
            count,
        )
