from typing import Optional

from application.dto import CollectionData
from config import ParserConfig

from .base import BaseParser


class PLSParser(BaseParser):
    _ext: str = "pls"

    def __init__(self, config: ParserConfig, url: Optional[str] = None):
        super().__init__(config)
        self.url: Optional[str] = url

    async def get_data(self) -> list[CollectionData]:
        if not self.url:
            raise ValueError("need set url,")

        global_name = self.url.rsplit(r"/", 1)[1].replace(self._ext, "")

        results = []
        data = await self.get_content(self.url)

        for url, name, tags in zip(*data):
            if not name:
                name = global_name
            results.append(CollectionData(name=name, url=url, info_data=tags))

        return results

    def get_data_from_file_data(self, data: str) -> tuple[list[str], list[str | None], list[list[str]]]:
        urls = {}
        titles = {}
        info_data: list[list[str]] = []

        for line in data.splitlines():
            line = line.strip()
            line_start = line[:5]

            if line_start.lower().startswith("file"):
                var, url = line.split("=")
                index = var.lower().replace("file", "")
                urls[index] = url

            if line_start.lower().startswith("title"):
                var, title = line.split("=")
                index = var.lower().replace("title", "")
                titles[index] = title

        result_urls = []
        result_names = []
        for index, url in urls.items():
            name: str | None = titles.get(index)
            result_urls.append(url)
            result_names.append(name)
            info_data.append([])

        return result_urls, result_names, info_data
