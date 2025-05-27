from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseUser(BaseData):
    hashed_password: Optional[str] = None
    google_id: Optional[str] = None

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


@dataclass(slots=True)
class CurrentUser(User):
    pass


@dataclass(slots=True)
class AdminUser(User):
    pass


@dataclass(slots=True)
class UpdateUser(BaseUser):
    email: Optional[str] = None


@dataclass(slots=True)
class AccessToken:
    value: str
