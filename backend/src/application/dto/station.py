from dataclasses import dataclass, field
from datetime import datetime

from application.types import StationStatusType

from fastapi import UploadFile

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class Station(BaseData):
    name: str
    url: str

    tags: list[str] = field(default_factory=list)
    status: StationStatusType = StationStatusType.NOT_VERIFIED

    @property
    def name_tags(self) -> str:
        if self.tags:
            return ",".join([self.name, *self.tags])
        return self.name


@dataclass(slots=True)
class StationData(Station):
    id: int

    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class UpdateStationStatus(BaseData):
    id: int
    status: StationStatusType


@dataclass(slots=True)
class StationsWithCount(BaseData):
    stations: list[StationData] = field(default_factory=list)
    count: int = 0


@dataclass(slots=True)
class BaseUploadStation(BaseData):
    user_id: int
    file_path: str


@dataclass(slots=True)
class UploadStation(BaseUploadStation):
    station: Station


@dataclass(slots=True)
class UploadStations(BaseUploadStation):
    stations: list[Station] = field(default_factory=list)


@dataclass(slots=True)
class UploadPlaylist(BaseUploadStation):
    file: UploadFile
