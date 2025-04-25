from typing import Any

from authlib.integrations.starlette_client import OAuth

from config import Config, GoogleConfig

from utils import SecurityTool


class Authenticator:

    def __init__(self, config: Config):
        self.config: GoogleConfig = config.google
        self.__security_tool: SecurityTool = SecurityTool(config.security)

        self.oauth = OAuth()
        self.oauth.register(
            name=self.config.google_client_name,
            client_id=self.config.google_client_id,
            client_secret=self.config.google_client_secret,
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
