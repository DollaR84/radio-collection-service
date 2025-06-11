import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor

from application.types import CheckerType

from .checkers import BaseChecker, CheckerProtocol
from .data import RadioTestData


class RadioTestExecutor:
    _executor = ThreadPoolExecutor(max_workers=10)

    def __init__(self, data: RadioTestData, checker_type: CheckerType, repeat_count: int, repeat_timeout: int):
        self.data = data
        self.timeout = repeat_timeout
        self.retries = repeat_count

        checker_cls = BaseChecker.get_checker(checker_type)
        self.checker: CheckerProtocol = checker_cls(self.data.url, self.timeout)

    async def check_stream(self) -> bool:
        for attempt in range(1, self.retries + 1):
            try:
                result = await asyncio.get_event_loop().run_in_executor(
                    self._executor,
                    self.checker
                )
                if result:
                    return True
                if attempt < self.retries:
                    await asyncio.sleep(self.timeout)
            except Exception as error:
                logging.warning("attempt %d failed for %s: %s", attempt, self.data.url, str(error))

        return False

    async def run(self) -> None:
        await asyncio.sleep(self.timeout)

        self.data.is_success = await self.check_stream()
        await self.data.callback_after(self.data)
