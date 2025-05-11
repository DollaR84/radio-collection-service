from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable


@dataclass(slots=True)
class RadioTestData:
    id: int
    url: str

    callback_after: Callable[[RadioTestData], Awaitable[None]]
    is_success: bool = False
