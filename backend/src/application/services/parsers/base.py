﻿from abc import ABC
import asyncio
import logging
import random

from aiohttp import ClientSession
import aiofiles
from fake_useragent import UserAgent

from application.dto import CollectionData, File

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

    async def get_data_from_file(self, file: File) -> list[list[CollectionData]]:
        full_data: list[CollectionData] = []

        if file.fileext.lower() != self._ext.lower():
            return [full_data]

        async with aiofiles.open(file.file_path_with_id, mode="r", encoding="utf-8") as file_data:
            data = self.get_data_from_file_data(await file_data.read())

            for url, name, tags in zip(*data):
                if not name:
                    name = file.filename
                full_data.append(CollectionData(name=name, url=url, info_data=tags))

        return self.get_batch_data(full_data)

    def get_data_from_file_data(self, _: str) -> tuple[list[str], list[str | None], list[list[str]]]:
        return [], [], []

    def get_batch_data(self, full_data: list[CollectionData]) -> list[list[CollectionData]]:
        data = []
        batch_data: list[CollectionData] = []

        for item in full_data:
            if len(batch_data) >= self.config.batch_size:
                data.append(batch_data)
                batch_data = []

            batch_data.append(item)
        data.append(batch_data)

        return data
