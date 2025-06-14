from datetime import datetime

from pydantic import BaseModel, Field

from application.types import StationStatusType


class StationResponse(BaseModel):
    id: int
    name: str
    url: str

    tags: list[str] = Field(default_factory=list)
    status: StationStatusType

    created_at: datetime
    updated_at: datetime


class StationsResponse(BaseModel):
    items: list[StationResponse] = Field(default_factory=list)
    total: int
