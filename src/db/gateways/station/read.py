from typing import Optional

from sqlalchemy import select

from db import domain

from ..base import BaseGateway

from ...models import Station


class GetStationGateway(BaseGateway[int, Station]):

    async def get_station(self, station_id: int) -> Optional[domain.StationModel]:
        stmt = select(Station)
        stmt = stmt.where(Station.id == station_id)
        error_message = "Error get station"

        station = await self._get(stmt, error_message)
        if station:
            return domain.StationModel(**station.dict(exclude=["id", "created_at", "updated_at"]))
        return None

    async def get_stations(self) -> list[domain.StationModel]:
        stmt = select(Station)
        error_message = "Error get stations"

        stations = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.StationModel(**station.dict(exclude=["id", "created_at", "updated_at"]))
            for station in stations
        ]

    async def get_stations_urls(self) -> list[str]:
        stations = await self.get_stations()
        return [station.url for station in stations]
