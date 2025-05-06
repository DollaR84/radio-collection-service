from dataclasses import dataclass, field

from .base import BaseData


@dataclass(slots=True)
class CollectionData(BaseData):
    name: str
    url: str
    info_data: list[str] = field(default_factory=list)

    def add_info(self, *data: str) -> None:
        for info in data:
            if info:
                self.info_data.append(info)
