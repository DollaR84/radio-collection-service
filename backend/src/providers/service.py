from dishka import from_context, Provider, Scope, provide

from application.services import CollectionParser, RadioTester, NoService

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
