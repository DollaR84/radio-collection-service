from dataclasses import dataclass, field

from application.types import StationStatusType

from .base import BaseData


@dataclass(slots=True)
class StationModel(BaseData):
    name: str
    url: str

    tags: list[str] = field(default_factory=list)
    status: StationStatusType = StationStatusType.NOT_VERIFIED
