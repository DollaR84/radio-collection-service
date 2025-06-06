from dataclasses import dataclass

from .base import BaseData


@dataclass(slots=True)
class AccessToken(BaseData):
    value: str
