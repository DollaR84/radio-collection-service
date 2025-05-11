import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import os
from typing import Awaitable, Callable

from config import TesterConfig

from .data import RadioTestData
from .executor import RadioTestExecutor


class RadioTester:

    def __init__(self, config: TesterConfig):
        self.config = config
        self.max_workers = min(32, (os.cpu_count() or 1) * 2 + 4)

        self.executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self.loop = asyncio.get_event_loop()

        self.logger = logging.getLogger()
        self.logger.info("thread pool stats: %d max workers", self.executor._max_workers)

    async def check(self, id_: int, url: str, callback_after: Callable[[RadioTestData], Awaitable[None]]) -> None:
        data = RadioTestData(id=id_, url=url, callback_after=callback_after)
        await self.loop.run_in_executor(
            self.executor,
            self._run_sync_check,
            data,
        )

    def _run_sync_check(self, data: RadioTestData) -> None:
        try:
            with RadioTestExecutor(data, self.config.repeat_count, self.config.repeat_timeout) as executor:
                executor.run()
        except Exception as error:
            self.logger.error("check failed for '%s': %s", data.url, str(error))
