from sqlalchemy import insert

from db import domain

from ..base import BaseGateway

from ...models import Station


class CreateStationGateway(BaseGateway[int, Station]):

    async def create_station(
            self,
            data: domain.StationModel,
    ) -> int:
        stmt = insert(Station).values(**data.dict(exclude_unset=True)).returning(Station.id)
        error_message = "Error creating new station"

        return await self._create(stmt, error_message)

    async def create_stations(
            self,
            data: list[domain.StationModel],
    ) -> list[int]:
        stations_data = [
            item.dict(exclude_unset=True)
            for item in data
        ]
        error_message = "Error creating new stations"

        stmt = insert(Station).values(stations_data).returning(Station.id)
        return await self._create(stmt, error_message, is_multiple=True)
