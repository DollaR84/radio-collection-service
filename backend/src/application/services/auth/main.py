from typing import Any

from authlib.integrations.starlette_client import OAuth

from fastapi import Request, Response

from application import dto
from application import interactors
from application.types import UserAccessRights

from config import Config, GoogleConfig

from .exceptions import NoJwtException, ForbiddenException
from .security import SecurityTool
from .types import TokenType


class Authenticator:

    def __init__(self, config: Config, request: Request):
        self.config: GoogleConfig = config.google
        self.__security_tool: SecurityTool = SecurityTool(config.security, request)

        self.oauth = OAuth()
        self.oauth.register(
            name=self.config.client_name,
            client_id=self.config.client_id,
            client_secret=self.config.client_secret,
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,
            api_base_url=self.api_base_url,
            client_kwargs={"scope": self.scopes},
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self.__security_tool, name)

    @property
    def access_token_url(self) -> str:
        return "https://accounts.google.com/o/oauth2/token"

    @property
    def authorize_url(self) -> str:
        return "https://accounts.google.com/o/oauth2/auth"

    @property
    def api_base_url(self) -> str:
        return "https://www.googleapis.com/oauth2/v1/"

    @property
    def scopes(self) -> str:
        return "openid email profile"

    def process_refresh_token(self, response: Response) -> dto.AccessToken:
        refresh_token = self.get_refresh_token()
        uuid_id = self.get_uuid_from_token(token=refresh_token, token_type=TokenType.REFRESH)
        access_token = self.set_access_token(uuid_id, response)
        return dto.AccessToken(value=access_token)

    def check_access_token(self, token: dto.AccessToken) -> None:
        self.check_expire_token(token=token.value, token_type=TokenType.ACCESS)

    async def get_current_user(
            self,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.CurrentUser:
        payload = self.check_expire_token(token=token.value, token_type=TokenType.ACCESS)
        uuid_id = self.get_uuid_from_token(payload=payload, token_type=TokenType.ACCESS)
        user = await interactor(uuid_id)

        if not user:
            raise NoJwtException()
        return dto.CurrentUser(**user.dict())

    async def get_current_admin_user(
            self,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.AdminUser:
        user = await self.get_current_user(interactor, token)
        if not user.is_admin or user.access_rights != UserAccessRights.OWNER:
            raise ForbiddenException()

        return dto.AdminUser(**user.dict())

    async def get_current_plus_user(
            self,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.PlusUser:
        user = await self.get_current_user(interactor, token)
        if user.access_rights not in (
            UserAccessRights.PLUS,
            UserAccessRights.PRO,
            UserAccessRights.FULL,
            UserAccessRights.OWNER,
        ):
            raise ForbiddenException()

        return dto.PlusUser(**user.dict())

    async def get_current_pro_user(
            self,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.ProUser:
        user = await self.get_current_user(interactor, token)
        if user.access_rights not in (
            UserAccessRights.PRO,
            UserAccessRights.FULL,
            UserAccessRights.OWNER,
        ):
            raise ForbiddenException()

        return dto.ProUser(**user.dict())

    async def get_current_full_user(
            self,
            interactor: interactors.GetUserByUUID,
            token: dto.AccessToken,
    ) -> dto.FullUser:
        user = await self.get_current_user(interactor, token)
        if user.access_rights not in (
            UserAccessRights.FULL,
            UserAccessRights.OWNER,
        ):
            raise ForbiddenException()

        return dto.FullUser(**user.dict())
