from typing import Any

from fastapi import Response

from application import dto

from .auth import AuthService
from .google import GoogleService
from .register import RegisterService
from .subscribe import SubscribeService
from .token import TokenService
from .exceptions import NotRegistered
from ... import schemas


class AuthOrchestrator:

    def __init__(
            self,
            auth: AuthService,
            register: RegisterService,
            google: GoogleService,
            subscribe: SubscribeService,
            token: TokenService,
    ):
        self.auth = auth
        self.register = register

        self.google = google
        self.subscribe = subscribe
        self.token = token

    async def __call__(
            self,
            data: schemas.UserCreateByPassword | schemas.UserLoginByPassword | schemas.UserGoogle | dict[str, Any],
            response: Response,
    ) -> schemas.AccessTokenResponse:
        if isinstance(data, dict):
            data = self.google.build_user_schema(data)

        if isinstance(data, schemas.UserCreateByPassword):
            user = await self.register(data)
        else:
            user = await self._authenticate(data)

        await self.subscribe(user, data.device_id)
        return self.token(user.uuid_id, response)

    async def _authenticate(self, data: schemas.UserLoginByPassword | schemas.UserGoogle) -> dto.User:
        user = await self.auth.get_user(data.email)

        if not user:
            if isinstance(data, schemas.UserGoogle):
                return await self.register(data)

            raise NotRegistered

        await self._handle_existing_user(user, data)
        return user

    async def _handle_existing_user(
            self,
            user: dto.User,
            data: schemas.UserLoginByPassword | schemas.UserGoogle,
    ) -> None:
        if isinstance(data, schemas.UserLoginByPassword):
            await self.auth(user, data)
        else:
            await self.google(user, data)
