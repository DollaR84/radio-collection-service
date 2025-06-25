from application.dto import AccessToken
from application.interactors import GetUserByUUID
from application.services import Authenticator
from application.services.auth.exceptions import NoJwtException, ForbiddenException

from config import Config

from sqladmin.authentication import AuthenticationBackend

from starlette.requests import Request


class AdminAuth(AuthenticationBackend):

    def __init__(self, config: Config):
        super().__init__(config.security.secret_key)

        self.config = config

    async def login(self, request: Request) -> bool:
        return True

    async def logout(self, request: Request) -> bool:
        return True

    async def authenticate(self, request: Request) -> bool:
        authenticator = Authenticator(self.config, request)

        try:
            token_value = authenticator.get_access_token()
            token = AccessToken(value=token_value)

            async with request.state.container() as container:
                get_user_by_uuid = await container.get(GetUserByUUID)
                await authenticator.get_current_admin_user(get_user_by_uuid, token)
                return True

        except (NoJwtException, ForbiddenException):
            return False
