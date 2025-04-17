from application.dto import CollectionData
from config import ParserConfig

from .base import BaseParser


class PLSParser(BaseParser):

    def __init__(self, config: ParserConfig, url: str):
        super().__init__(config)
        self.url: str = url

    async def get_data(self) -> list[CollectionData]:
        results = []
        data = await self.get_content(self.url)
        urls = {}
        titles = {}

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

        for index, url in urls.items():
            title = titles.get(index, "")

            results.append(CollectionData(name=title, url=url))

        return results
