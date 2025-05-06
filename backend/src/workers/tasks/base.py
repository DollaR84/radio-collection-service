from __future__ import annotations

from abc import ABC, abstractmethod
import re
from typing import Any, Optional, Type

from apscheduler.triggers.base import BaseTrigger


class BaseTask(ABC):
    _tasks: dict[str, Type[BaseTask]] = {}
    order_id: int = 0
    trigger: Optional[BaseTrigger] = None

    def __init_subclass__(cls, is_abstract: bool = False, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if is_abstract:
            return

        name = cls.get_name()
        if name not in cls._tasks:
            cls._tasks[name] = cls

    @classmethod
    def get_name(cls) -> str:
        name = cls.__name__.replace("Task", "")
        return " ".join(list(re.findall(r"[A-Z][a-z0-9]+", name)))

    @classmethod
    def get_task(cls, name: str) -> Type[BaseTask]:
        task_cls = cls._tasks.get(name)
        if task_cls is None:
            raise ValueError(f"Task '{name}' not found")
        return task_cls

    @classmethod
    def get_all_tasks(cls) -> list[Type[BaseTask]]:
        return sorted(
            cls._tasks.values(),
            key=lambda x: x.order_id
        )

    @abstractmethod
    async def execute(self) -> None:
        raise NotImplementedError
