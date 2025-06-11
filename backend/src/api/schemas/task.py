from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class TaskRequest(BaseModel):
    name: str


class TaskResponse(BaseModel):
    job_id: str


class TaskJobStatus(TaskResponse):
    status: str


class TaskJobResult(TaskResponse):
    task_name: str

    success: bool
    job_try: int

    enqueue_time: datetime
    start_time: Optional[datetime]
    finish_time: Optional[datetime]

    score: Optional[int] = None
    result: Optional[Any] = None
    progress: Optional[Any] = None
