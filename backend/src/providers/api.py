from dishka import from_context, Provider, Scope, provide

from fastapi import Request, Response

from application import dto
from application import interactors
from application.services import Authenticator

from config import Config


class ApiProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)
    request = from_context(provides=Request, scope=Scope.REQUEST)
    response = from_context(provides=Response, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_auth(self, config: Config, request: Request, response: Response) -> Authenticator:
        return Authenticator(config, request, response)

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
    ) -> dto.CurrentUser:
        user = await auth.get_current_user(interactor)
        return user

    @provide(scope=Scope.REQUEST)
    async def get_current_admin_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
    ) -> dto.AdminUser:
        user = await auth.get_current_admin_user(interactor)
        return user
