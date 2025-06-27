from dishka import from_context, Provider, Scope, provide

from application import interactors
from application.services import CollectionParser, NoService, RadioTester, Resolver, Uploader

from config import Config


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)

    no_service = provide(NoService, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_collection_parser(self, config: Config) -> CollectionParser:
        return CollectionParser(config.parser)

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
            config: Config,
            get_urls: interactors.GetStationUrls,
            creator: interactors.CreateStations,
    ) -> Uploader:
        return Uploader(config.parser, get_urls, creator)
