from typing import Optional

from application import dto
from application import interfaces
from application.types import StationStatusType


class BaseGetStation:

    def __init__(self, gateway: interfaces.GetStationInterface):
        self.gateway = gateway


class GetStations(BaseGetStation):

    async def __call__(
            self,
            user: dto.User,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[dto.Station]:
        stations = await self.gateway.get_stations(user, name, info, status, offset, limit)
        return [
            dto.Station(**station.dict(exclude=["id", "created_at", "updated_at"]))
            for station in stations
        ]


class GetStationUrls(BaseGetStation):

    async def __call__(self) -> list[str]:
        return await self.gateway.get_stations_urls()
