from dataclasses import dataclass, field
from datetime import datetime

from application.types import StationStatusType

from .base import BaseData


@dataclass(slots=True)
class StationModel(BaseData):
    id: int

    name: str
    url: str

    created_at: datetime
    updated_at: datetime

    tags: list[str] = field(default_factory=list)
    status: StationStatusType = StationStatusType.NOT_VERIFIED
