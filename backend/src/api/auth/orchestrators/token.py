import uuid

from fastapi import Response

from application.services import Authenticator

from ... import schemas


class TokenService:

    def __init__(self, auth: Authenticator):
        self.auth = auth

    def __call__(self, uuid_id: uuid.UUID, response: Response) -> schemas.AccessTokenResponse:
        access_token = self.auth.set_access_token(uuid_id, response)
        self.auth.set_refresh_token(uuid_id, response)

        return schemas.AccessTokenResponse(access_token=access_token)
