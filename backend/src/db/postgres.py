from contextlib import asynccontextmanager
import logging
import ssl
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.exc import OperationalError

from config import DBConfig

from .base import BaseDbConnector


class PostgresDbConnector(BaseDbConnector):

    def __init__(self, config: DBConfig):
        connect_args = {}
        if config.ssl:
            ssl_context = ssl.create_default_context()
            connect_args["ssl"] = ssl_context

        try:
            self._engine = create_async_engine(
                config.uri,
                echo=config.debug,
                pool_size=15,
                max_overflow=15,
                connect_args=connect_args,
            )
        except Exception as error:
            logger = logging.getLogger()
            logger.error(error, exc_info=True)
            raise ValueError("Error: failed to create engine") from error

        self._session_factory = async_sessionmaker(
            bind=self._engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:  # pylint: disable=invalid-overridden-method
        async with self._session_factory() as session:
            try:
                yield session

            except Exception as error:
                await session.rollback()
                raise OperationalError(statement=str(error), params=None, orig=error) from error

            finally:
                await session.aclose()
