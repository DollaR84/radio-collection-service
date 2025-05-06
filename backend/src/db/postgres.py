from asyncio import current_task
from contextlib import asynccontextmanager
import logging
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, async_scoped_session
from sqlalchemy.exc import OperationalError

from config import DBConfig

from .base import Base, BaseDbConnector


class PostgresDbConnector(BaseDbConnector):

    def __init__(self, config: DBConfig):
        try:
            self._engine = create_async_engine(
                config.uri,
                echo=config.debug,
                pool_size=15,
                max_overflow=15,
            )
        except Exception as error:
            logger = logging.getLogger()
            logger.error(error, exc_info=True)
            raise ValueError("Error: failed to create engine") from error

        self._session_factory = async_sessionmaker(
            binds={Base: self._engine},
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:  # pylint: disable=invalid-overridden-method
        session = async_scoped_session(self._session_factory, scopefunc=current_task)()
        try:
            yield session

        except Exception as error:
            await session.rollback()
            raise OperationalError(statement=str(error), params=None, orig=error) from error

        finally:
            await session.aclose()
