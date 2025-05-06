from dataclasses import dataclass, field
from datetime import datetime

from application.types import StationStatusType

from .base import BaseData


@dataclass(slots=True)
class Station(BaseData):
    name: str
    url: str

    tags: list[str] = field(default_factory=list)
    status: StationStatusType = StationStatusType.NOT_VERIFIED


class StationData(Station):
    id: int

    created_at: datetime
    updated_at: datetime
