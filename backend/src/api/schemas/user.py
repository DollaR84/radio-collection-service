from datetime import datetime
import uuid
from typing import Optional
from typing_extensions import Self

from pydantic import BaseModel, EmailStr, Field, model_validator

from application.types import UserAccessRights


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

    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[str] = None
    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    access_rights: Optional[UserAccessRights] = None


class PasswordUpdate(BaseModel):
    new_password: str
    confirm_password: str
    current_password: Optional[str] = None


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

    has_password: bool = False
    access_rights: UserAccessRights = UserAccessRights.DEFAULT


class UserMessageResponse(BaseModel):
    ok: bool
    message: str


class UserAccessRightsSchema(UserResponse):
    access_rights: UserAccessRights = UserAccessRights.DEFAULT
    expires_at: Optional[datetime] = None
