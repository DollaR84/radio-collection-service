from abc import ABC
import asyncio
import logging
import os
import random

from aiohttp import ClientSession
from fake_useragent import UserAgent

from application.dto import CollectionData

from config import ParserConfig


class BaseParser(ABC):
    _ext: str

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

    def get_data_from_file(self, file_path: str) -> list[CollectionData]:
        results: list[CollectionData] = []

        file_name, file_ext = os.path.splitext(file_path)
        if file_ext.lower() != self._ext.lower():
            return results

        with open(file_path, "r", encoding="utf-8") as file_data:
            data = self.get_data_from_file_data(file_data.read())

            for url, name in zip(*data):
                if not name:
                    name = file_name
                results.append(CollectionData(name=name, url=url))

        return results

    def get_data_from_file_data(self, _: str) -> tuple[list[str], list[str | None]]:
        return [], []
