import logging

from dishka import from_context, Provider, Scope, provide

from fastapi import Request
from fastapi.security import OAuth2PasswordBearer

from api.auth.orchestrators import (
    AuthOrchestrator,
    AuthService,
    GoogleService,
    RegisterService,
    SubscribeService,
    TokenService,
)

from application import dto
from application import interactors
from application.services import Authenticator, Resolver

from config import Config


class ApiProvider(Provider):

    config = from_context(provides=Config, scope=Scope.APP)
    oauth2_scheme = from_context(provides=OAuth2PasswordBearer, scope=Scope.APP)
    request = from_context(provides=Request, scope=Scope.REQUEST)

    @provide(scope=Scope.REQUEST)
    async def get_access_token(
            self,
            request: Request,
            auth: Authenticator,
            oauth2_scheme: OAuth2PasswordBearer,
    ) -> dto.AccessToken:
        token = await oauth2_scheme(request)
        if token:
            token = token.replace("Bearer", "").strip()
        else:
            token = auth.get_access_token(request)

        if token is None:
            raise ValueError("token not found")
        return dto.AccessToken(value=token)

    @provide(scope=Scope.APP)
    async def get_auth(self, config: Config) -> Authenticator:
        return Authenticator(config)

    @provide(scope=Scope.REQUEST)
    async def get_auth_orchestrator(
            self,
            auth: AuthService,
            register: RegisterService,
            google: GoogleService,
            subscribe: SubscribeService,
            token: TokenService,
    ) -> AuthOrchestrator:
        return AuthOrchestrator(auth, register, google, subscribe, token)

    @provide(scope=Scope.REQUEST)
    async def get_auth_service(self, auth: Authenticator, interactor: interactors.GetUserByEmail) -> AuthService:
        return AuthService(auth, interactor)

    @provide(scope=Scope.REQUEST)
    async def get_google_service(self, updater: interactors.UpdateUserByUUID) -> GoogleService:
        return GoogleService(updater)

    @provide(scope=Scope.REQUEST)
    async def get_register_service(
            self,
            auth: Authenticator,
            creator: interactors.CreateUser,
            interactor: interactors.GetUserByUUID,
    ) -> RegisterService:
        return RegisterService(auth, creator, interactor)

    @provide(scope=Scope.REQUEST)
    async def get_subscribe_service(
            self,
            resolver: Resolver,
            updater: interactors.UpdateUserByUUID,
    ) -> SubscribeService:
        return SubscribeService(resolver, updater)

    @provide(scope=Scope.REQUEST)
    async def get_token_service(self, auth: Authenticator) -> TokenService:
        return TokenService(auth)

    @provide(scope=Scope.REQUEST)
    async def get_current_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.CurrentUser:
        user = await auth.get_current_user(interactor, token)
        logging.info("current user id=%d: %s", user.id, user.user_name or user.email)
        return user

    @provide(scope=Scope.REQUEST)
    async def get_current_admin_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.AdminUser:
        user = await auth.get_current_admin_user(interactor, token)
        logging.info("current admin user id=%d: %s", user.id, user.user_name or user.email)
        return user

    @provide(scope=Scope.REQUEST)
    async def get_current_plus_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.PlusUser:
        user = await auth.get_current_plus_user(interactor, token)
        logging.info("current plus user id=%d: %s", user.id, user.user_name or user.email)
        return user

    @provide(scope=Scope.REQUEST)
    async def get_current_pro_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.ProUser:
        user = await auth.get_current_pro_user(interactor, token)
        logging.info("current pro user id=%d: %s", user.id, user.user_name or user.email)
        return user

    @provide(scope=Scope.REQUEST)
    async def get_current_full_user(
            self,
            auth: Authenticator,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.FullUser:
        user = await auth.get_current_full_user(interactor, token)
        logging.info("current full user id=%d: %s", user.id, user.user_name or user.email)
        return user
