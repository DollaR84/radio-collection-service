from dataclasses import dataclass

from .base import BaseData


@dataclass(slots=True)
class UploadFile(BaseData):
    filename: str
    id: int | None = None


@dataclass(slots=True)
class UploadM3UFile(UploadFile):
    pass


@dataclass(slots=True)
class UploadPLSFile(UploadFile):
    pass
