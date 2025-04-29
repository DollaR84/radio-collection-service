from dataclasses import dataclass
from typing import Optional
import uuid

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseUser(BaseData):
    email: str
    hashed_password: Optional[str] = None
    google_id: Optional[str] = None

    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class NewUser(BaseUser):
    pass


@dataclass(slots=True)
class User(BaseUser):
    id: int
    uuid_id: uuid.UUID

    is_active: bool
    is_admin: bool
