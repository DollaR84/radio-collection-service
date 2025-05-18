from typing import Any, Literal, Optional

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dishka import AsyncContainer

from .manager import TaskManager


class ArqContext(dict):
    __slots__ = ("scheduler", "task_manager", "dishka_container",)

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

        self.scheduler: Optional[AsyncIOScheduler] = None
        self.task_manager: Optional[TaskManager] = None
        self.dishka_container: Optional[AsyncContainer] = None

    def __getattr__(self, name: str) -> Any:
        try:
            return self[name]
        except KeyError as error:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'") from error

    def __setattr__(self, name: Literal["scheduler", "task_manager"] | str, value: Any) -> None:
        if name in self.__slots__:  # Разрешаем установку атрибутов из slots
            super().__setattr__(name, value)
        else:
            self[name] = value

    def __contains__(self, key: object) -> bool:
        return super().__contains__(key) or hasattr(self, str(key))

    def __dir__(self) -> list[str]:
        base_dir = list(super().__dir__())
        keys_as_str = [str(k) for k in self.keys()]
        return base_dir + keys_as_str
