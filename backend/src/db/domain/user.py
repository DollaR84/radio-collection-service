from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseUserModel(BaseData):
    user_name: Optional[str] = None
    hashed_password: Optional[str] = None

    google_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass(slots=True)
class BaseEmailUserModel(BaseUserModel):
    email: str


@dataclass(slots=True)
class NewUserModel(BaseEmailUserModel):
    pass


@dataclass(slots=True)
class UserModel(BaseEmailUserModel):
    id: int
    uuid_id: uuid.UUID

    created_at: datetime
    updated_at: datetime

    is_active: bool
    is_admin: bool


@dataclass(slots=True)
class UpdateUserModel(BaseUserModel):
    email: Optional[str] = None
