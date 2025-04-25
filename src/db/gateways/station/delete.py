from sqlalchemy import delete

from ..base import BaseGateway

from ...models import Station


class DeleteStationGateway(BaseGateway[int, Station]):

    async def delete_station(
            self,
            station_id: int,
    ) -> None:
        stmt = delete(Station)
        stmt = stmt.where(Station.id == station_id)

        error_message = f"Error deleting station id={station_id}"
        await self._delete(stmt, error_message)
