from datetime import datetime

from pydantic import BaseModel, Field

from application.types import StationStatusType


class BaseStation(BaseModel):
    name: str
    url: str

    tags: list[str] = Field(default_factory=list)


class StationResponse(BaseStation):
    id: int
    status: StationStatusType

    created_at: datetime
    updated_at: datetime


class StationsResponse(BaseModel):
    items: list[StationResponse] = Field(default_factory=list)
    total: int


class StationRequest(BaseStation):
    pass


class StationsRequest(BaseModel):
    items: list[StationRequest] = Field(default_factory=list)


class StationsSavingResponse(BaseModel):
    count: int
