from typing import AsyncGenerator

from dishka import from_context, Provider, Scope, provide

from sqlalchemy.ext.asyncio import AsyncSession

from application import interfaces

from config import Config

from db import DbConnector
from db.base import BaseDbConnector
from db import gateways


class DBProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_db(self, config: Config) -> BaseDbConnector:
        return DbConnector(config.db)

    @provide(scope=Scope.REQUEST)
    async def db_session(self, connector: DbConnector) -> AsyncGenerator[AsyncSession, None]:
        async with connector.get_session() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def user_creator(self, session: AsyncSession) -> interfaces.CreateUserInterface:
        return gateways.CreateUserGateway(session)

    @provide(scope=Scope.REQUEST)
    async def user_deleter(self, session: AsyncSession) -> interfaces.DeleteUserInterface:
        return gateways.DeleteUserGateway(session)

    @provide(scope=Scope.REQUEST)
    async def station_creator(self, session: AsyncSession) -> interfaces.CreateStationInterface:
        return gateways.CreateStationGateway(session)

    @provide(scope=Scope.REQUEST)
    async def station_deleter(self, session: AsyncSession) -> interfaces.DeleteStationInterface:
        return gateways.DeleteStationGateway(session)

    @provide(scope=Scope.REQUEST)
    async def station_getter(self, session: AsyncSession) -> interfaces.GetStationInterface:
        return gateways.GetStationGateway(session)
