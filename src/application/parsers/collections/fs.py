from typing import Any

from application.dto import CollectionData

from .base import BaseCollection

from ..m3u import M3UParser


class FileSystemCollection(BaseCollection):
    order_id: int = 4

    def __init__(self, name: str, **kwargs: Any):
        super().__init__(name, **kwargs)

    def make_url(self, **kwargs: Any) -> str:
        return ""

    async def load(self, url: str) -> list[CollectionData]:
        return []

    async def process_data(self, url: str) -> list[CollectionData]:
        results: list[CollectionData] = []
        if not url:
            return results

        parser = M3UParser(self.parser.config, base_path=url)
        results.extend(await parser.get_data())

        return results
