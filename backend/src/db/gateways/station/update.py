from sqlalchemy import case, update

from db import domain

from ..base import BaseGateway

from ...models import Station


class UpdateStationGateway(BaseGateway[int, Station]):

    async def update_station_status(self, update_data: domain.UpdateStationStatusModel) -> int:
        error_message = f"Error update station status id={update_data.id}"

        stmt = update(Station)
        stmt = stmt.where(Station.id == update_data.id)
        stmt = stmt.values(status=update_data.status)
        stmt = stmt.returning(Station.id)

        return await self._update(stmt, error_message)

    async def update_stations_status(self, update_data: list[domain.UpdateStationStatusModel]) -> list[int]:
        error_message = "Error update stations status"
        if not update_data:
            return []

        whens = {
            Station.id == item.id: item.status
            for item in update_data
        }

        stmt = update(Station)
        stmt = stmt.where(Station.id.in_([item.id for item in update_data]))
        stmt = stmt.values(status=case(whens, value=Station.id))
        stmt = stmt.returning(Station.id)

        return await self._update(stmt, error_message, is_multiple=True)
