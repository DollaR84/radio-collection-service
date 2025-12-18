from dataclasses import dataclass
from datetime import datetime
from typing import Literal, Optional
import uuid

from application.types import UserAccessRights

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseUser(BaseData):
    hashed_password: Optional[str] = None
    google_id: Optional[str] = None
    device_id: Optional[str] = None

    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass(slots=True)
class BaseEmailUser(BaseUser):
    email: str


@dataclass(slots=True)
class NewUser(BaseEmailUser):
    pass


@dataclass(slots=True)
class User(BaseEmailUser):
    id: int
    uuid_id: uuid.UUID

    is_active: bool
    is_admin: bool

    created_at: datetime
    updated_at: datetime

    access_rights: UserAccessRights = UserAccessRights.DEFAULT


@dataclass(slots=True)
class CurrentUser(User):
    is_admin: Literal[False]


@dataclass(slots=True)
class AdminUser(User):
    is_admin: Literal[True]
    access_rights: Literal[UserAccessRights.FULL, UserAccessRights.OWNER]


@dataclass(slots=True)
class UpdateUser(BaseUser):
    email: Optional[str] = None
    access_rights: Optional[UserAccessRights] = None


@dataclass(slots=True)
class UpdatePassword(BaseData):
    hashed_password: str


@dataclass(slots=True)
class PlusUser(User):
    access_rights: Literal[UserAccessRights.PLUS]


@dataclass(slots=True)
class ProUser(User):
    access_rights: Literal[UserAccessRights.PRO]


@dataclass(slots=True)
class FullUser(User):
    access_rights: Literal[UserAccessRights.FULL]


@dataclass(slots=True)
class OwnerUser(User):
    access_rights: Literal[UserAccessRights.OWNER]
