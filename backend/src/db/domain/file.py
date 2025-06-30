from dataclasses import dataclass
from datetime import datetime
from typing import Literal

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseFileModel(BaseData):
    user_id: int
    file_path: str
    filename: str
    fileext: str
    file_id: str
    is_load: bool = False


@dataclass(slots=True)
class NewFileModel(BaseFileModel):
    pass


@dataclass(slots=True)
class FileModel(BaseFileModel):
    id: int
    created_at: datetime


@dataclass(slots=True)
class UpdateFileModel(BaseData):
    is_load: Literal[True]
