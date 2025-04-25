from typing import Optional

from arq.connections import RedisSettings, create_pool

from dishka import from_context, Provider, Scope, provide

from application.services import Authenticator, CollectionParser

from config import Config

from workers import TaskManager


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)
    task_manager: Optional[TaskManager] = None

    @provide(scope=Scope.REQUEST)
    async def get_auth(self, config: Config) -> Authenticator:
        return Authenticator(config)

    @provide(scope=Scope.REQUEST)
    async def get_collection_parser(self, config: Config) -> CollectionParser:
        return CollectionParser(config.parser)

    @provide(scope=Scope.REQUEST)
    async def get_task_manager(self) -> TaskManager:
        if self.task_manager is None:
            redis_pool = await create_pool(RedisSettings(host="redis"))
            self.task_manager = TaskManager(redis_pool=redis_pool)
            self.task_manager.register_adhoc_tasks()
        return self.task_manager
