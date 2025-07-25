from typing import Optional

from dishka import AsyncContainer, from_context, Provider, Scope, provide

from application.interactors import (
    CreateStations,
    GetStations,
    CheckStationUrl,
    UpdateStationsStatus,
    GetM3uFilesForParse,
    GetPlsFilesForParse,
    UpdateFileLoadStatus,
)
from application.services import CollectionParser, M3UParser, PLSParser, RadioTester

from config import Config

from workers import TaskManager
from workers.tasks import (
    RadioBrowserTask,
    InternetRadioStreamsTask,
    Mp3RadioStationsTask,
    M3uPlaylistTask,
    PlsPlaylistTask,
    TestNotVerifiedTask,
    TestNotWorkTask,
    TestWorksTask,
)


class TaskProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)
    container = from_context(provides=AsyncContainer, scope=Scope.APP)
    task_manager: Optional[TaskManager] = None

    @provide(scope=Scope.REQUEST)
    async def get_task_manager(self, config: Config, container: AsyncContainer) -> TaskManager:
        if self.task_manager is None:
            self.task_manager = TaskManager()
            self.task_manager.dishka_container = container
            await self.task_manager.create_redis_pool(config)
            self.task_manager.register_adhoc_tasks()
        return self.task_manager

    @provide(scope=Scope.REQUEST)
    async def get_radio_browser_task(
            self,
            parser: CollectionParser,
            check_station_url: CheckStationUrl,
            creator: CreateStations,
    ) -> RadioBrowserTask:
        return RadioBrowserTask(parser, check_station_url, creator)

    @provide(scope=Scope.REQUEST)
    async def get_internet_radio_streams_task(
            self,
            parser: CollectionParser,
            check_station_url: CheckStationUrl,
            creator: CreateStations,
    ) -> InternetRadioStreamsTask:
        return InternetRadioStreamsTask(parser, check_station_url, creator)

    @provide(scope=Scope.REQUEST)
    async def get_mp3_radio_stations_task(
            self,
            parser: CollectionParser,
            check_station_url: CheckStationUrl,
            creator: CreateStations,
    ) -> Mp3RadioStationsTask:
        return Mp3RadioStationsTask(parser, check_station_url, creator)

    @provide(scope=Scope.REQUEST)
    async def get_m3u_playlist_task(
            self,
            parser: M3UParser,
            get_m3u_files: GetM3uFilesForParse,
            check_station_url: CheckStationUrl,
            creator: CreateStations,
            update_status: UpdateFileLoadStatus,
    ) -> M3uPlaylistTask:
        return M3uPlaylistTask(parser, get_m3u_files, check_station_url, creator, update_status)

    @provide(scope=Scope.REQUEST)
    async def get_pls_playlist_task(
            self,
            parser: PLSParser,
            get_pls_files: GetPlsFilesForParse,
            check_station_url: CheckStationUrl,
            creator: CreateStations,
            update_status: UpdateFileLoadStatus,
    ) -> PlsPlaylistTask:
        return PlsPlaylistTask(parser, get_pls_files, check_station_url, creator, update_status)

    @provide(scope=Scope.REQUEST)
    async def get_test_not_verified_task(
            self,
            tester: RadioTester,
            get_stations: GetStations,
            updater: UpdateStationsStatus,
    ) -> TestNotVerifiedTask:
        return TestNotVerifiedTask(tester, get_stations, updater)

    @provide(scope=Scope.REQUEST)
    async def get_test_not_work_task(
            self,
            tester: RadioTester,
            get_stations: GetStations,
            updater: UpdateStationsStatus,
    ) -> TestNotWorkTask:
        return TestNotWorkTask(tester, get_stations, updater)

    @provide(scope=Scope.REQUEST)
    async def get_test_works_task(
            self,
            tester: RadioTester,
            get_stations: GetStations,
            updater: UpdateStationsStatus,
    ) -> TestWorksTask:
        return TestWorksTask(tester, get_stations, updater)
