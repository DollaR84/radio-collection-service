import logging

from dishka import from_context, Provider, Scope, provide

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

from application import dto
from application import interactors
from application.services import Authenticator

from config import Config


class ApiProvider(Provider):
    scope = Scope.REQUEST

    config = from_context(provides=Config, scope=Scope.APP)
    oauth2_scheme = from_context(provides=OAuth2PasswordBearer, scope=Scope.APP)
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_access_token(
            self,
            request: Request,
            config: Config,
            auth: Authenticator,
            oauth2_scheme: OAuth2PasswordBearer,
    ) -> dto.AccessToken:
        if config.security.cookie.is_enable:
            token = auth.get_access_token()
        else:
            token = await oauth2_scheme(request)
            token = token.replace("Bearer", "").strip()

        return dto.AccessToken(value=token)

    @provide(scope=Scope.REQUEST)
    async def get_auth(self, config: Config, request: Request) -> Authenticator:
        return Authenticator(config, request)

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.CurrentUser:
        user = await auth.get_current_user(interactor, token)
        logging.info("current user: %d", user.id)
        return user

    @provide(scope=Scope.REQUEST)
    async def get_current_admin_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.AdminUser:
        user = await auth.get_current_admin_user(interactor, token)
        logging.info("current admin user: %d", user.id)
        return user
