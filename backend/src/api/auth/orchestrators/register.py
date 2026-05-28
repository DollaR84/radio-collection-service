import uuid

from application import dto
from application import interactors
from application.services import Authenticator

from .exceptions import EmailIsExists, NotRegistered
from ... import schemas


class RegisterService:

    def __init__(
            self,
            auth: Authenticator,
            creator: interactors.CreateUser,
            interactor: interactors.GetUserByUUID,
    ):
        self.auth = auth
        self.creator = creator
        self.interactor = interactor

    async def __call__(self, data: schemas.UserCreateByPassword | schemas.UserGoogle) -> dto.User:
        user_data = self._build_user_dto(data)
        uuid_id = await self._create_user(user_data)
        user = await self.interactor(uuid_id)

        if not user:
            raise NotRegistered
        return user

    def _build_user_dto(self, data: schemas.UserCreateByPassword | schemas.UserGoogle) -> dto.NewUser:
        if isinstance(data, schemas.UserCreateByPassword):
            return dto.NewUser(
                email=data.email,
                user_name=data.user_name,
                hashed_password=self.auth.get_password_hash(data.password)
            )

        if isinstance(data, schemas.UserGoogle):
            return dto.NewUser(
                email=data.email,
                google_id=data.google_id,
                first_name=data.first_name,
                last_name=data.last_name,
            )

        raise TypeError("Unsupported registration type")

    async def _create_user(self, user_data: dto.NewUser) -> uuid.UUID:
        try:
            return await self.creator(user_data)
        except Exception as error:
            raise EmailIsExists from error
