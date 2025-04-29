import uuid
from typing import Optional
from typing_extensions import Self

from pydantic import BaseModel, EmailStr, Field, model_validator


class BaseUser(BaseModel):
    email: EmailStr


class UserCreateByPassword(BaseUser):
    user_name: str
    password: str = Field(min_length=5, max_length=50, description="Password, from 5 to 50 symbols")
    confirm_password: str = Field(min_length=5, max_length=50, description="Confirm password")

    @model_validator(mode="after")
    def check_password(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("passwords do not match")
        return self


class UserLoginByPassword(BaseUser):
    password: str = Field(min_length=5, max_length=50, description="Password, from 5 to 50 symbols")


class UserGoogle(BaseUser):
    google_id: str


class UserResponse(BaseModel):
    uuid_id: uuid.UUID


class UserInfoResponse(UserResponse):
    id: int
    email: EmailStr
    google_id: Optional[str] = None

    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    is_active: bool
    is_admin: bool


class UserMessageResponse(BaseModel):
    ok: bool
    message: str
