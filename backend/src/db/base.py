from abc import ABC, abstractmethod
from typing import Any, AsyncContextManager, Dict, List

from sqlalchemy.ext.asyncio import AsyncAttrs, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, declared_attr
import sqlalchemy.orm as so

from utils.text import pascal_case_to_snake_case


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:  # pylint: disable=no-self-argument
        return pascal_case_to_snake_case(cls.__name__) + "s"

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
    _engine: AsyncEngine

    @property
    def engine(self) -> AsyncEngine:
        return self._engine

    @abstractmethod
    def get_session(self) -> AsyncContextManager[AsyncSession]:
        raise NotImplementedError
