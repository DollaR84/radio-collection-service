from dishka import from_context, Provider, Scope, provide

from config import Config

from db import DbConnector
from db.base import BaseDbConnector


class DBProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_db(self, config: Config) -> BaseDbConnector:
        return DbConnector(config)
