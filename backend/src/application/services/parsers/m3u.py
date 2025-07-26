import logging
import os
from typing import Optional

import aiofiles

from application.dto import CollectionData
from config import ParserConfig

from .base import BaseParser


class M3UParser(BaseParser):
    _ext: str = "m3u"

    def __init__(
            self,
            config: ParserConfig,
            url: Optional[str] = None,
            name: Optional[str] = None,
            base_path: Optional[str] = None,
    ):
        super().__init__(config)
        self.url = url
        self.name = name
        self.base_path = base_path

        if self.url and not self.name:
            self.name = self.url.rsplit(r"/", 1)[1].replace(self._ext, "")

    async def get_data(self) -> list[CollectionData]:
        results: list[CollectionData] = []

        if self.url:
            data = await self.get_data_from_url()
        elif self.base_path:
            data = await self.get_data_from_path(self.base_path)
        else:
            return results

        for global_name, data_items in data.items():
            for url, name, tags in zip(*data_items):
                if not name:
                    name = global_name
                results.append(CollectionData(name=name, url=url, info_data=tags))

        return results

    async def get_data_from_url(self) -> dict[str, tuple[list[str], list[str | None], list[list[str]]]]:
        if not isinstance(self.url, str) or not isinstance(self.name, str):
            raise ValueError("need to specify 'url' and 'name' on m3u file")

        data = await self.get_content(self.url)
        return {self.name: self.get_data_from_file_data(data)}

    async def get_data_from_path(self, folder: str) -> dict[str, tuple[list[str], list[str | None], list[list[str]]]]:
        results = {}

        subfolders = [subfolder for subfolder in os.listdir(folder) if os.path.isdir(os.path.join(folder, subfolder))]
        files = [file for file in os.listdir(folder) if os.path.isfile(os.path.join(folder, file))]

        for file in files:
            try:
                file_name, file_ext = os.path.splitext(file)
                if file_ext.lower() != ".m3u":
                    continue

                async with aiofiles.open(os.path.join(folder, file), mode="r", encoding="utf-8") as file_data:
                    results[file_name] = self.get_data_from_file_data(await file_data.read())
            except Exception as error:
                logger = logging.getLogger()
                logger.error("Error read file: %s in %s", file, folder)
                logger.error(error, exc_info=True)

        for subfolder in subfolders:
            results.update(await self.get_data_from_path(os.path.join(folder, subfolder)))

        return results

    def get_data_from_file_data(self, data: str) -> tuple[list[str], list[str | None], list[list[str]]]:
        urls = []
        names = []
        info_data = []

        current_name = None
        tags = []
        for line in data.splitlines():
            line = line.strip()
            line_start = line[:8]

            if line_start.lower().startswith("#extinf:"):
                extinfo = line.split(",")
                if len(extinfo) > 1:
                    current_name = extinfo[1]
                    tags.extend(extinfo[2:] if len(extinfo) > 2 else [])

            if line_start.lower().startswith("http"):
                urls.append(line)
                names.append(current_name)
                info_data.append(tags.copy())
                current_name = None
                tags.clear()

        return urls, names, info_data
