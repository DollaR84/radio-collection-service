import json
import os
from typing import Optional

import aiofiles

from application.dto import CollectionData
from config import ParserConfig

from .base import BaseParser


class JsonParser(BaseParser):
    _ext: str = "json"

    def __init__(self, config: ParserConfig, file_path: Optional[str] = None):
        super().__init__(config)
        self.file_path: Optional[str] = file_path

    async def get_data(self) -> list[CollectionData]:
        if not self.file_path:
            raise ValueError("file path must be set before parsing")

        file_name, _ = os.path.splitext(self.file_path)

        results = []
        async with aiofiles.open(self.file_path, mode="r", encoding="utf-8") as file_data:
            data = self.get_data_from_file_data(await file_data.read())

            for url, name, tags in zip(*data):
                if not name:
                    name = file_name
                results.append(CollectionData(name=name, url=url, info_data=tags))

        return results

    def get_data_from_file_data(self, data: str) -> tuple[list[str], list[str | None], list[list[str]]]:
        urls = {}
        names = {}
        info_data: list[list[str]] = []

        items = json.loads(data)
        for index, item in enumerate(items):
            urls[index] = item["url"]
            names[index] = item["name"]
            info_data.append(item["tags"].copy())

        result_urls = []
        result_names = []
        for index, url in urls.items():
            name: str | None = names.get(index)
            result_urls.append(url)
            result_names.append(name)

        return result_urls, result_names, info_data
