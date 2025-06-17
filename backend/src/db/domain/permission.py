from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from application.types import UserAccessRights

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseAccessPermissionModel(BaseData):
    access_rights: UserAccessRights = UserAccessRights.DEFAULT
    reason: Optional[str] = None

    user_id: Optional[int] = None
    expires_at: Optional[datetime] = None


@dataclass(slots=True)
class CreateAccessPermissionModel(BaseAccessPermissionModel):
    user_id: int
    expires_at: datetime


@dataclass(slots=True)
class AccessPermissionModel(BaseAccessPermissionModel):
    user_id: int
    expires_at: datetime

    id: int
    created_at: datetime


@dataclass(slots=True)
class UpdateAccessPermissionModel(BaseAccessPermissionModel):
    pass
