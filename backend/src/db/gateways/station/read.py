from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import func, select, exists
from sqlalchemy.sql import Select

from application.types import StationStatusType, LastType

from db import domain

from ..base import BaseGateway

from ...models import Station, Favorite


class GetStationGateway(BaseGateway[int, Station]):

    async def get_station(self, station_id: int) -> Optional[domain.StationModel]:
        error_message = f"Error get station id={station_id}"

        stmt = select(Station)
        stmt = stmt.where(Station.id == station_id)

        station = await self._get(stmt, error_message)
        return domain.StationModel(**station.dict()) if station else None

    async def get_stations(
            self,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
            last: Optional[LastType] = None,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.StationModel]:
        error_message = "Error get stations"
        stmt = select(Station)

        stmt = self._build_conditions(stmt, name, info, status, last)
        stmt = stmt.order_by(Station.id.desc())

        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        stations = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.StationModel(**station.dict())
            for station in stations
        ]

    async def get_count(
            self,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
            last: Optional[LastType] = None,
    ) -> int:
        error_message = "error getting stations count"
        stmt = select(func.count(Station.id))  # pylint: disable=not-callable
        stmt = self._build_conditions(stmt, name, info, status, last)
        return await self._get_count(stmt, error_message)

    async def get_double_name(self) -> list[domain.StationModel]:
        subquery = select(Station.name)
        subquery = subquery.group_by(Station.name)
        subquery = subquery.having(func.count(Station.url) > 1)  # pylint: disable=not-callable

        stmt = select(Station)
        stmt = stmt.where(Station.name.in_(select(subquery.subquery().c.name)))

        error_message = "error getting stations with double naming"
        stations = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.StationModel(**station.dict())
            for station in stations
        ]

    def _build_conditions(
            self,
            stmt: Select,
            name: Optional[str] = None,
            info: Optional[str] = None,
            status: Optional[StationStatusType] = None,
            last: Optional[LastType] = None,
    ) -> Select:
        if name:
            stmt = stmt.where(Station.name.icontains(name))

        if info:
            stmt = stmt.where(
                func.array_to_string(Station.tags, ',').ilike(f"%{info}%")
            )

        if status:
            stmt = stmt.where(Station.status == status)

        if last and last != LastType.NOTHING:
            cutoff_date = datetime.now() - timedelta(days=last)
            stmt = stmt.where(Station.created_at >= cutoff_date)

        return stmt


class GetStationsUrlsGateway(BaseGateway[int, str]):

    async def get_stations_urls(
            self,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[str]:
        error_message = "Error get stations"
        stmt = select(Station.url)

        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        urls = await self._get(stmt, error_message, is_multiple=True)
        return urls

    async def check_station_url(self, url: str) -> bool:
        error_message = f"Error check station url: '{url}'"
        stmt = select(exists().where(Station.url == url))
        return await self._get_exists(stmt, error_message)


class GetFavoriteGateway(BaseGateway[int, Station]):

    async def get_favorites(
            self,
            user_id: int,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[domain.StationModel]:
        error_message = f"Error get favorites for user id={user_id}"
        stmt = select(Station)

        stmt = self._build_conditions(stmt, user_id)
        stmt = stmt.order_by(Favorite.id)

        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        stations = await self._get(stmt, error_message, is_multiple=True)
        return [
            domain.StationModel(**station.dict())
            for station in stations
        ]

    async def get_count(self, user_id: int) -> int:
        error_message = f"error getting favorites count for user id={user_id}"
        stmt = select(func.count(Station.id))  # pylint: disable=not-callable
        stmt = self._build_conditions(stmt, user_id)
        return await self._get_count(stmt, error_message)

    def _build_conditions(
            self,
            stmt: Select,
            user_id: int,
    ) -> Select:
        stmt = stmt.join(Favorite, Favorite.station_id == Station.id)
        stmt = stmt.where(Favorite.user_id == user_id)
        return stmt
