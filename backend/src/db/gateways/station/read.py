from typing import Optional

from sqlalchemy import select, exists, func

from application import dto
from application.types import StationStatusType

from db import domain

from ..base import BaseGateway

from ...models import Station


class GetStationGateway(BaseGateway[int, Station]):

    async def get_station(self, station_id: int) -> Optional[domain.StationModel]:
        error_message = "Error get station"

        stmt = select(Station)
        stmt = stmt.where(Station.id == station_id)

        station = await self._get(stmt, error_message)
        if station:
            return domain.StationModel(**station.dict(exclude=["id", "created_at", "updated_at"]))
        return None

    async def get_stations(
            self,
            user: dto.User,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.StationModel]:
        error_message = f"Error get stations for user id={user.id}"
        stmt = select(Station)

        if name:
            stmt = stmt.where(Station.name.icontains(name))
        if info:
            stmt = stmt.where(
                exists().where(
                    func.unnest(Station.tags).icontains(info)
                )
            )
        if status:
            stmt = stmt.where(Station.status == status)

        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        stations = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.StationModel(**station.dict())
            for station in stations
        ]

    async def get_stations_urls(self) -> list[str]:
        error_message = "Error get stations"
        stmt = select(Station)

        stations = await self._get(stmt, error_message, is_multiple=True)
        return [station.url for station in stations]
