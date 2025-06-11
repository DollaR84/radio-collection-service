import asyncio
import logging
from typing import Awaitable, Callable

from config import TesterConfig

from .data import RadioTestData
from .executor import RadioTestExecutor


class RadioTester:

    def __init__(self, config: TesterConfig):
        self.config = config
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent_tasks)

    async def check(self, id_: int, url: str, callback_after: Callable[[RadioTestData], Awaitable[None]]) -> None:
        async with self.semaphore:
            data = RadioTestData(id=id_, url=url, callback_after=callback_after)

            executor = RadioTestExecutor(
                data,
                checker_type=self.config.checker_type,
                repeat_count=self.config.repeat_count,
                repeat_timeout=self.config.repeat_timeout
            )

            try:
                await executor.run()
            except Exception as error:
                logging.error("check failed for %s: %s", url, str(error))
                data.is_success = False
                await callback_after(data)
