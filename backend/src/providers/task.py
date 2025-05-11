from typing import Optional

from arq.connections import RedisSettings, create_pool

from dishka import AsyncContainer, from_context, Provider, Scope, provide

from application.interactors import CreateStation, GetStations, GetStationUrls, UpdateStationStatus
from application.services import CollectionParser, RadioTester

from config import Config

from workers import TaskManager
from workers.tasks import (
    RadioBrowserTask,
    InternetRadioStreamsTask,
    Mp3RadioStationsTask,
    TestNotVerifiedTask,
    TestNotWorkTask,
)


class TaskProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)
    container = from_context(provides=AsyncContainer, scope=Scope.APP)
    task_manager: Optional[TaskManager] = None

    @provide(scope=Scope.REQUEST)
    async def get_task_manager(self, config: Config, container: AsyncContainer) -> TaskManager:
        if self.task_manager is None:
            redis_pool = await create_pool(RedisSettings(
                host=config.redis.host,
                port=config.redis.port,
                database=config.worker.redis_database,
            ))
            self.task_manager = TaskManager(redis_pool=redis_pool, container=container)
            self.task_manager.register_adhoc_tasks()
        return self.task_manager

    @provide(scope=Scope.REQUEST)
    async def get_radio_browser_task(
            self,
            parser: CollectionParser,
            get_urls: GetStationUrls,
            creator: CreateStation,
    ) -> RadioBrowserTask:
        return RadioBrowserTask(parser, get_urls, creator)

    @provide(scope=Scope.REQUEST)
    async def get_internet_radio_streams_task(
            self,
            parser: CollectionParser,
            get_urls: GetStationUrls,
            creator: CreateStation,
    ) -> InternetRadioStreamsTask:
        return InternetRadioStreamsTask(parser, get_urls, creator)

    @provide(scope=Scope.REQUEST)
    async def get_mp3_radio_stations_task(
            self,
            parser: CollectionParser,
            get_urls: GetStationUrls,
            creator: CreateStation,
    ) -> Mp3RadioStationsTask:
        return Mp3RadioStationsTask(parser, get_urls, creator)

    @provide(scope=Scope.REQUEST)
    async def get_test_not_verified_task(
            self,
            tester: RadioTester,
            get_stations: GetStations,
            updater: UpdateStationStatus,
    ) -> TestNotVerifiedTask:
        return TestNotVerifiedTask(tester, get_stations, updater)

    @provide(scope=Scope.REQUEST)
    async def get_test_not_work_task(
            self,
            tester: RadioTester,
            get_stations: GetStations,
            updater: UpdateStationStatus,
    ) -> TestNotWorkTask:
        return TestNotWorkTask(tester, get_stations, updater)
