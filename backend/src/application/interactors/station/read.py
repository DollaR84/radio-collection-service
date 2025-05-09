from typing import Optional

from application import dto
from application import interfaces
from application.types import StationStatusType


class BaseGetStation:

    def __init__(self, gateway: interfaces.GetStationInterface):
        self.gateway = gateway


class GetStation(BaseGetStation):

    async def __call__(self, station_id: int) -> Optional[dto.Station]:
        station = await self.gateway.get_station(station_id)
        return dto.Station(**station.dict(exclude=["id", "created_at", "updated_at"])) if station else None


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


class GetStationUrls:

    def __init__(self, gateway: interfaces.GetStationsUrlsInterface):
        self.gateway = gateway

    async def __call__(self) -> list[str]:
        return await self.gateway.get_stations_urls()


class GetUserFavorites:

    def __init__(self, gateway: interfaces.GetFavoriteInterface):
        self.gateway = gateway

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
