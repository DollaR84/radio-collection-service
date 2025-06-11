from __future__ import annotations

from abc import ABC, abstractmethod
import logging
import subprocess
from typing import Any, Protocol, Type

from application.types import CheckerType


class CheckerProtocol(Protocol):

    def __call__(self) -> bool:
        ...


class BaseChecker(ABC):
    _checkers: dict[str, Type[BaseChecker]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        name = cls.get_name()
        if name not in cls._checkers and not kwargs.get("is_abstract"):
            cls._checkers[name] = cls

    @classmethod
    def get_name(cls) -> str:
        _name = cls.__name__.replace("Checker", "")
        return _name.lower()

    @classmethod
    def get_checker(cls, checker_type: CheckerType) -> Type[BaseChecker]:
        return cls._checkers[checker_type.value]

    def __init__(self, url: str, timeout: float):
        self.url: str = url
        self.timeout: float = timeout

    def close(self) -> None:
        pass

    @abstractmethod
    def __call__(self) -> bool:
        raise NotImplementedError


class BaseFFMpegChecker(BaseChecker, is_abstract=True):

    def run(self, command: list[str]) -> bool:
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=self.timeout,
                encoding="utf-8",
                errors="ignore"
            )
            return result.returncode == 0

        except subprocess.TimeoutExpired as error:
            logging.debug("timeout checking %s: %s", self.url, str(error))
            return False

        except subprocess.CalledProcessError as error:
            logging.debug("process error checking %s: %s", self.url, str(error))
            return False

        except Exception as error:
            logging.error("FFprobe error for %s: %s", self.url, str(error))
            return False
