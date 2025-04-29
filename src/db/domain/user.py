from dataclasses import dataclass
from typing import Optional
import uuid

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseUserModel(BaseData):
    email: str
    user_name: Optional[str] = None
    hashed_password: Optional[str] = None

    google_id: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class NewUserModel(BaseUserModel):
    pass


@dataclass(slots=True)
class UserModel(BaseUserModel):
    id: int
    uuid_id: uuid.UUID

    is_active: bool
    is_admin: bool
