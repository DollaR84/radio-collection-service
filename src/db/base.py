from abc import ABC, abstractmethod
from typing import Any, AsyncContextManager, Dict, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
import sqlalchemy.orm as so

from utils.text import paschal_case_to_snake_case


class Base(DeclarativeBase):

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not cls.__tablename__:
            cls.__tablename__ = paschal_case_to_snake_case(cls.__name__) + "s"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} #{self.id}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__} #{self.id}"

    def dict(self, exclude_unset: bool = False, exclude: List[str] | None = None) -> Dict[str, Any]:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}

        if exclude_unset:
            data = {key: value for key, value in data.items() if value is not None}

        if exclude:
            data = {key: value for key, value in data.items() if key not in exclude}

        return data


class BaseDbConnector(ABC):

    @abstractmethod
    def get_session(self) -> AsyncContextManager[AsyncSession]:
        raise NotImplementedError
