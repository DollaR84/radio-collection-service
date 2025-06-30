from typing import AsyncGenerator

from dishka import from_context, Provider, Scope, provide

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from application import interfaces

from config import Config

from db import PostgresDbConnector
from db.base import BaseDbConnector
from db import gateways


class DBProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    async def get_db(self, config: Config) -> BaseDbConnector:
        return PostgresDbConnector(config.db)

    @provide(scope=Scope.APP)
    async def get_db_engine(self, db: BaseDbConnector) -> AsyncEngine:
        return db.engine

    @provide(scope=Scope.REQUEST)
    async def db_session(self, connector: BaseDbConnector) -> AsyncGenerator[AsyncSession, None]:
        async with connector.get_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def user_creator(self, session: AsyncSession) -> interfaces.CreateUserInterface:
        return gateways.CreateUserGateway(session)

    @provide(scope=Scope.REQUEST)
    async def user_deleter(self, session: AsyncSession) -> interfaces.DeleteUserInterface:
        return gateways.DeleteUserGateway(session)

    @provide(scope=Scope.REQUEST)
    async def user_getter(self, session: AsyncSession) -> interfaces.GetUserInterface:
        return gateways.GetUserGateway(session)

    @provide(scope=Scope.REQUEST)
    async def user_updater(self, session: AsyncSession) -> interfaces.UpdateUserInterface:
        return gateways.UpdateUserGateway(session)

    @provide(scope=Scope.REQUEST)
    async def station_creator(self, session: AsyncSession) -> interfaces.CreateStationInterface:
        return gateways.CreateStationGateway(session)

    @provide(scope=Scope.REQUEST)
    async def station_deleter(self, session: AsyncSession) -> interfaces.DeleteStationInterface:
        return gateways.DeleteStationGateway(session)

    @provide(scope=Scope.REQUEST)
    async def station_getter(self, session: AsyncSession) -> interfaces.GetStationInterface:
        return gateways.GetStationGateway(session)

    @provide(scope=Scope.REQUEST)
    async def stations_urls_getter(self, session: AsyncSession) -> interfaces.GetStationsUrlsInterface:
        return gateways.GetStationsUrlsGateway(session)

    @provide(scope=Scope.REQUEST)
    async def station_updater(self, session: AsyncSession) -> interfaces.UpdateStationInterface:
        return gateways.UpdateStationGateway(session)

    @provide(scope=Scope.REQUEST)
    async def favorite_creator(self, session: AsyncSession) -> interfaces.CreateFavoriteInterface:
        return gateways.CreateFavoriteGateway(session)

    @provide(scope=Scope.REQUEST)
    async def favorite_deleter(self, session: AsyncSession) -> interfaces.DeleteFavoriteInterface:
        return gateways.DeleteFavoriteGateway(session)

    @provide(scope=Scope.REQUEST)
    async def favorite_getter(self, session: AsyncSession) -> interfaces.GetFavoriteInterface:
        return gateways.GetFavoriteGateway(session)

    @provide(scope=Scope.REQUEST)
    async def access_permission_creator(self, session: AsyncSession) -> interfaces.CreateAccessPermissionInterface:
        return gateways.CreateAccessPermissionGateway(session)

    @provide(scope=Scope.REQUEST)
    async def access_permission_deleter(self, session: AsyncSession) -> interfaces.DeleteAccessPermissionInterface:
        return gateways.DeleteAccessPermissionGateway(session)

    @provide(scope=Scope.REQUEST)
    async def access_permission_getter(self, session: AsyncSession) -> interfaces.GetAccessPermissionInterface:
        return gateways.GetAccessPermissionGateway(session)

    @provide(scope=Scope.REQUEST)
    async def access_permission_updater(self, session: AsyncSession) -> interfaces.UpdateAccessPermissionInterface:
        return gateways.UpdateAccessPermissionGateway(session)

    @provide(scope=Scope.REQUEST)
    async def file_creator(self, session: AsyncSession) -> interfaces.CreateFileInterface:
        return gateways.CreateFileGateway(session)

    @provide(scope=Scope.REQUEST)
    async def file_deleter(self, session: AsyncSession) -> interfaces.DeleteFileInterface:
        return gateways.DeleteFileGateway(session)

    @provide(scope=Scope.REQUEST)
    async def file_getter(self, session: AsyncSession) -> interfaces.GetFileInterface:
        return gateways.GetFileGateway(session)

    @provide(scope=Scope.REQUEST)
    async def file_updater(self, session: AsyncSession) -> interfaces.UpdateFileInterface:
        return gateways.UpdateFileGateway(session)
