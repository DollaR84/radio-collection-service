from sqlalchemy import bindparam, func, literal_column, select, update, union_all
from sqlalchemy.dialects.postgresql import ENUM

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

        temp_updates = union_all(
            *[
                select(
                    literal_column(str(item.id)).label("id"),
                    bindparam(
                        "status_val",
                        item.status.name,
                        type_=ENUM(name="station_status_type", create_type=False)
                    ).label("status")
                )
                for item in update_data
            ]
        ).alias("temp_updates")

        stmt = update(Station)
        stmt = stmt.where(Station.id == temp_updates.c.id)
        stmt = stmt.values(status=temp_updates.c.status, updated_at=func.now())  # pylint: disable=not-callable
        stmt = stmt.returning(Station.id)

        return await self._update(stmt, error_message, is_multiple=True)
