from dishka import from_context, Provider, Scope, provide

from application.services import Authenticator

from config import Config


class ServiceProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)

    @provide(scope=Scope.REQUEST)
    async def get_auth(self, config: Config) -> Authenticator:
        return Authenticator(config)
