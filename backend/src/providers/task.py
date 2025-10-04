from typing import Optional

from dishka import AsyncContainer, from_context, Provider, Scope, provide

from application.interactors import (
    CreateStations,
    GetStations,
    GetStationUrls,
    UpdateStationsStatus,
    GetM3uFilesForParse,
    GetPlsFilesForParse,
    GetJsonFilesForParse,
    UpdateFileLoadStatus,
    GetUsers,
    GetCurrentAccessPermission,
    UpdateUserByID,
)
from application.services import CollectionParser, M3UParser, PLSParser, JsonParser, RadioTester

from config import Config

from workers import TaskManager
from workers.tasks import (
    RadioBrowserTask,
    InternetRadioStreamsTask,
    Mp3RadioStationsTask,
    M3uPlaylistTask,
    PlsPlaylistTask,
    JsonPlaylistTask,
    PermissionDefaultTask,
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
            get_all_urls: GetStationUrls,
            creator: CreateStations,
    ) -> RadioBrowserTask:
        return RadioBrowserTask(parser, get_all_urls, creator)

    @provide(scope=Scope.REQUEST)
    async def get_internet_radio_streams_task(
            self,
            parser: CollectionParser,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
    ) -> InternetRadioStreamsTask:
        return InternetRadioStreamsTask(parser, get_all_urls, creator)

    @provide(scope=Scope.REQUEST)
    async def get_mp3_radio_stations_task(
            self,
            parser: CollectionParser,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
    ) -> Mp3RadioStationsTask:
        return Mp3RadioStationsTask(parser, get_all_urls, creator)

    @provide(scope=Scope.REQUEST)
    async def get_m3u_playlist_task(
            self,
            parser: M3UParser,
            get_m3u_files: GetM3uFilesForParse,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
            update_status: UpdateFileLoadStatus,
    ) -> M3uPlaylistTask:
        return M3uPlaylistTask(parser, get_m3u_files, get_all_urls, creator, update_status)

    @provide(scope=Scope.REQUEST)
    async def get_pls_playlist_task(
            self,
            parser: PLSParser,
            get_pls_files: GetPlsFilesForParse,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
            update_status: UpdateFileLoadStatus,
    ) -> PlsPlaylistTask:
        return PlsPlaylistTask(parser, get_pls_files, get_all_urls, creator, update_status)

    @provide(scope=Scope.REQUEST)
    async def get_json_playlist_task(
            self,
            parser: JsonParser,
            get_json_files: GetJsonFilesForParse,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
            update_status: UpdateFileLoadStatus,
    ) -> JsonPlaylistTask:
        return JsonPlaylistTask(parser, get_json_files, get_all_urls, creator, update_status)

    @provide(scope=Scope.REQUEST)
    async def get_permission_default_task(
            self,
            get_users: GetUsers,
            get_current_permission: GetCurrentAccessPermission,
            updater: UpdateUserByID,
    ) -> PermissionDefaultTask:
        return PermissionDefaultTask(get_users, get_current_permission, updater)

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
