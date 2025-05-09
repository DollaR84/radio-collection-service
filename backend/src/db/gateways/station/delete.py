from sqlalchemy import delete

from ..base import BaseGateway

from ...models import Station, Favorite


class DeleteStationGateway(BaseGateway[int, Station]):

    async def delete_station(
            self,
            station_id: int,
    ) -> None:
        stmt = delete(Station)
        stmt = stmt.where(Station.id == station_id)

        error_message = f"Error deleting station id={station_id}"
        await self._delete(stmt, error_message)


class DeleteFavoriteGateway(BaseGateway[int, Favorite]):

    async def delete_favorite(
            self,
            user_id: int,
            station_id: int,
    ) -> None:
        stmt = delete(Favorite)
        stmt = stmt.where(
            Favorite.user_id == user_id,
            Favorite.station_id == station_id
        )

        error_message = f"Error deleting favorite user_id={user_id}, station_id={station_id}"
        await self._delete(stmt, error_message)
