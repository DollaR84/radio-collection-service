from dataclasses import dataclass
from typing import Optional
import uuid

from .base import BaseData


@dataclass(slots=True)
class NewUser(BaseData):
    email: str
    hashed_password: Optional[str] = None
    google_id: Optional[str] = None

    user_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass(slots=True)
class User(BaseData):
    uuid_id: uuid.UUID
