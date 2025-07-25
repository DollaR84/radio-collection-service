from typing import Optional

from dishka import from_context, Provider, Scope, provide

from application import interactors
from application import Templater
from application.services import (
    CollectionParser,
    M3UParser,
    PLSParser,
    JsonParser,
    NoService,
    RadioTester,
    Resolver,
    Uploader,
)

from config import Config


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)

    no_service = provide(NoService, scope=Scope.REQUEST)
    templater: Optional[Templater] = None

    @provide(scope=Scope.APP)
    async def get_templater(self) -> Templater:
        if self.templater is None:
            self.templater = Templater()
        return self.templater

    @provide(scope=Scope.REQUEST)
    async def get_collection_parser(self, config: Config) -> CollectionParser:
        return CollectionParser(config.parser)

    @provide(scope=Scope.REQUEST)
    async def get_m3u_parser(self, config: Config) -> M3UParser:
        return M3UParser(config.parser)

    @provide(scope=Scope.REQUEST)
    async def get_pls_parser(self, config: Config) -> PLSParser:
        return PLSParser(config.parser)

    @provide(scope=Scope.REQUEST)
    async def get_json_parser(self, config: Config) -> JsonParser:
        return JsonParser(config.parser)

    @provide(scope=Scope.REQUEST)
    async def get_radio_tester(self, config: Config) -> RadioTester:
        return RadioTester(config.tester)

    @provide(scope=Scope.REQUEST)
    async def get_resolver(
            self,
            config: Config,
            creator: interactors.CreateAccessPermission,
            getter: interactors.GetAccessPermission,
            getters: interactors.GetAccessPermissions,
            updator: interactors.UpdateAccessPermission,
    ) -> Resolver:
        return Resolver(config.resolver, creator, getter, getters, updator)

    @provide(scope=Scope.REQUEST)
    async def get_uploader(
            self,
            templater: Templater,
            create_file: interactors.CreateFile,
    ) -> Uploader:
        return Uploader(templater, create_file)
