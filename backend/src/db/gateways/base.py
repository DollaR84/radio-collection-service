import logging
from typing import Generic, Literal, Optional, overload, TypeVar
import uuid

from sqlalchemy.exc import SQLAlchemyError, MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete, Insert, Select


T = TypeVar("T", int, uuid.UUID)
M = TypeVar("M")


class BaseGateway(Generic[T, M]):

    def __init__(self, session: AsyncSession):
        self.session = session

    @overload
    async def _create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: Literal[False] = False,
    ) -> T:
        ...

    @overload
    async def _create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: Literal[True],
    ) -> list[T]:
        ...

    async def _create(
            self,
            stmt: Insert,
            error_message: str,
            is_multiple: bool = False,
    ) -> T | list[T]:
        try:
            result = await self.session.execute(stmt)
            await self.session.commit()

            return list(result.scalars().all()) if is_multiple else result.scalar_one()
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    async def _delete(self, stmt: Delete, error_message: str) -> None:
        try:
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error

    @overload
    async def _get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: Literal[False] = False,
    ) -> Optional[M]:
        ...

    @overload
    async def _get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: Literal[True],
    ) -> list[M]:
        ...

    async def _get(
            self,
            stmt: Select,
            error_message: str,
            is_multiple: bool = False,
    ) -> Optional[M] | list[M]:
        try:
            result = await self.session.execute(stmt)

            return list(result.scalars().all()) if is_multiple else result.scalar_one_or_none()
        except MultipleResultsFound as error:
            logging.error(error, exc_info=True)
            raise ValueError(f"Multiple records found: {error_message}") from error

        except SQLAlchemyError as error:
            logging.error(error, exc_info=True)
            raise ValueError(error_message) from error
