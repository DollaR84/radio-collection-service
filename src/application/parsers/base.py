from abc import ABC
import asyncio
import logging
import random

from aiohttp import ClientSession
from fake_useragent import UserAgent

from config import ParserConfig


class BaseParser(ABC):

    def __init__(self, config: ParserConfig):
        self.config: ParserConfig = config
        self.ua = UserAgent()

        random.seed()

    @property
    def headers(self) -> dict[str, str]:
        return {
            "User-Agent": self.ua.chrome,
        }

    async def sleep(self) -> None:
        timeout = random.random() + self.config.default_sleep_timeout
        await asyncio.sleep(timeout)

    async def get_content(self, url: str) -> str:
        content = ""

        try:
            async with ClientSession(headers=self.headers) as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.text()
                    await self.sleep()

        except Exception as error:
            logging.error(error, exc_info=True)

        return content
