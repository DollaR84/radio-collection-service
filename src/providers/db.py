from dishka import from_context, Provider, Scope, provide

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
    async def create_user(self, db: BaseDbConnector) -> interfaces.CreateUser:
        async with db.get_session() as session:
            return gateways.CreateUserGateway(session)

    @provide(scope=Scope.REQUEST)
    async def delete_user(self, db: BaseDbConnector) -> interfaces.DeleteUser:
        async with db.get_session() as session:
            return gateways.DeleteUserGateway(session)
