from pydantic import BaseModel


class TaskData(BaseModel):
    name: str


class TaskStartedResponse(BaseModel):
    job_id: str
