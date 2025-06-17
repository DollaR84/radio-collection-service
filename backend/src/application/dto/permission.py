from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.types import UserAccessRights

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseAccessPermission(BaseData):
    user_id: Optional[int] = None
    expires_at: Optional[datetime] = None

    access_rights: UserAccessRights = UserAccessRights.DEFAULT
    reason: Optional[str] = None


@dataclass(slots=True)
class CreateAccessPermission(BaseAccessPermission):
    user_id: int
    expires_at: datetime


@dataclass(slots=True)
class AccessPermission(BaseAccessPermission):
    id: int
    user_id: int
    expires_at: datetime
    created_at: datetime


@dataclass(slots=True)
class UpdateAccessPermission(BaseAccessPermission):
    pass
