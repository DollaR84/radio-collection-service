import logging
from typing import Any, Optional

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

    async def load(self, url: str, offset: Optional[int] = None, limit: Optional[int] = None) -> list[CollectionData]:
        results = []

        counter = 0
        for data in self.client.stations():
            if offset and counter < offset:
                continue

            item = CollectionData(
                name=data.get("name", "").replace("\t", "").replace("\n", "").strip(),
                url=data.get("url", ""),
            )
            item.add_info(data.get("country"), data.get("countrycode"), str(data.get("bitrate", 0)), data.get("codec"))
            results.append(item)

            counter += 1
            if limit and len(results) == limit:
                break

        return results

    async def process_data(
            self,
            url: str,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
    ) -> list[CollectionData]:
        results = []
        try:
            results.extend(await self.load(url, offset, limit))

        except Exception as error:
            logging.error(error, exc_info=True)

        return results
