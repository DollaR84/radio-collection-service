from typing import Optional

from application import dto
from application import interactors
from application.services import Authenticator

from .exceptions import IncorrectLoginData
from ... import schemas


class AuthService:

    def __init__(self, auth: Authenticator, interactor: interactors.GetUserByEmail):
        self.auth = auth
        self.interactor = interactor

    async def get_user(self, email: str) -> Optional[dto.User]:
        return await self.interactor(email)

    async def __call__(self, user: dto.User, data: schemas.UserLoginByPassword) -> None:
        await self._authenticate_user(user, data)

    async def _authenticate_user(self, user: dto.User, data: schemas.UserLoginByPassword) -> None:
        if not self.auth.verify_password(plain_password=data.password, hashed_password=user.hashed_password):
            raise IncorrectLoginData
