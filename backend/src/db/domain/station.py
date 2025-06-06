from dataclasses import dataclass, field
from datetime import datetime

from application.types import StationStatusType

from .base import BaseData


@dataclass(slots=True)
class CreateStationModel(BaseData):
    name: str
    url: str

    status: StationStatusType = StationStatusType.NOT_VERIFIED
    tags: list[str] = field(default_factory=list)


@dataclass(slots=True)
class StationModel(BaseData):
    id: int

    name: str
    url: str

    created_at: datetime
    updated_at: datetime

    tags: list[str] = field(default_factory=list)
    status: StationStatusType = StationStatusType.NOT_VERIFIED


@dataclass(slots=True)
class UpdateStationStatusModel(BaseData):
    id: int
    status: StationStatusType
