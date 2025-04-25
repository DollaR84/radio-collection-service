import logging
from typing import Any

from pyradios import RadioBrowser

from application.dto import CollectionData

from .base import BaseCollection


class RadioBrowserCollection(BaseCollection):
    order_id: int = 1

    def __init__(self, name: str, **kwargs: Any):
        super().__init__(name, **kwargs)

        self.client: RadioBrowser = RadioBrowser()

    def make_url(self, **kwargs: Any) -> str:
        return ""

    async def load(self, url: str) -> list[CollectionData]:
        results = []

        for data in self.client.stations():
            item = CollectionData(
                name=data.get("name", "").replace("\t", "").replace("\n", "").strip(),
                url=data.get("url", ""),
            )
            item.add_info(data.get("country"), data.get("countrycode"), str(data.get("bitrate", 0)), data.get("codec"))
            results.append(item)

        return results

    async def process_data(self, url: str) -> list[CollectionData]:
        results = []
        try:
            results.extend(await self.load(url))

        except Exception as error:
            logging.error(error, exc_info=True)

        return results
