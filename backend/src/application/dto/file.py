from dataclasses import dataclass
from datetime import datetime
import os

from .base import BaseData


@dataclass(slots=True, kw_only=True)
class BaseFile(BaseData):
    user_id: int
    file_path: str
    filename: str
    fileext: str
    is_load: bool = False


@dataclass(slots=True)
class NewFile(BaseFile):
    file_id: str

    @property
    def file_path_with_id(self) -> str:
        return os.path.join(self.file_path, f"{self.file_id}.{self.fileext}")


@dataclass(slots=True)
class File(NewFile):
    id: int
    created_at: datetime
