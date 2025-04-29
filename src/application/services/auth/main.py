from typing import Any

from authlib.integrations.starlette_client import OAuth

from fastapi import Request

from application import dto
from application import interactors

from config import Config, GoogleConfig

from .exceptions import NoJwtException, ForbiddenException
from .security import SecurityTool


class Authenticator:

    def __init__(self, config: Config):
        self.config: GoogleConfig = config.google
        self.__security_tool: SecurityTool = SecurityTool(config.security)

        self.check_refresh_token = self.__security_tool.check_refresh_token

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

    async def get_user_by_refresh_token(self, request: Request, get_user: interactors.GetUserByUUID) -> dto.User:
        token = self.get_access_token(request)
        uuid_id = self.get_uuid_from_token(token)
        user = await get_user(uuid_id)

        if not user:
            raise NoJwtException
        return user

    async def get_current_user(self, request: Request, get_user: interactors.GetUserByUUID) -> dto.User:
        token = self.get_access_token(request)
        uuid_id = self.check_expire_refresh_token(token)
        user = await get_user(uuid_id)

        if not user:
            raise NoJwtException
        return user

    async def get_current_admin_user(self, request: Request, get_user: interactors.GetUserByUUID) -> dto.User:
        token = self.get_access_token(request)
        user = await self.get_current_user(token, get_user)
        if not user.is_admin:
            raise ForbiddenException

        return user
