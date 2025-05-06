from datetime import datetime

from pydantic import BaseModel, Field

from application.types import StationStatusType


class StationResponse(BaseModel):
    id: int
    name: str
    url: str
    tags: list[str] = Field(default_factory=list)
    status: StationStatusType = StationStatusType.NOT_VERIFIED

    created_at: datetime
    updated_at: datetime
