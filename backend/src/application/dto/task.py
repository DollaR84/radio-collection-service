from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional

from .base import BaseData


@dataclass(slots=True)
class JobResult(BaseData):
    job_id: str
    task_name: str

    job_try: int
    success: bool

    start_time: Optional[datetime]
    finish_time: Optional[datetime]
    enqueue_time: datetime

    score: Optional[int] = None
    result: Optional[Any] = None
