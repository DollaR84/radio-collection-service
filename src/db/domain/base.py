from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class BaseData:

    def dict(self, exclude_unset: bool = False, exclude: list | None = None) -> dict[str, Any]:
        result = {}

        for key, value in asdict(self).items():
            if key.startswith("_"):
                key = key[1:]
                value = getattr(self, key)

            if exclude_unset and value is None:
                continue

            if exclude and key in exclude:
                continue

            result[key] = value
        return result
