import json
import logging
import os
from typing import Any, Optional

from pyradios import RadioBrowser

from application.dto import CollectionData

from .base import BaseCollection


class RadioBrowserCollection(BaseCollection):
    order_id: int = 1

    def __init__(self, name: str, **kwargs: Any):
        super().__init__(name, **kwargs)

        self.client: RadioBrowser = RadioBrowser()
        self.need_update: bool = True

    def make_url(self, **kwargs: Any) -> str:
        return ""

    @property
    def file_path(self) -> str:
        return os.path.join(self.parser.config.upload_folder, "radio_browser.json")

    def _load(self) -> None:
        data = self.client.stations()

        with open(self.file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file)

        self.need_update = False

    async def load(self, url: str, offset: Optional[int] = None, limit: Optional[int] = None) -> list[CollectionData]:
        results = []
        if self.need_update:
            self._load()

        stations = []
        with open(self.file_path, "r", encoding="utf-8") as json_file:
            stations = json.load(json_file)

        if offset and limit and offset < len(stations):
            stations = stations[offset:limit]
        elif offset and offset >= len(stations):
            os.remove(self.file_path)
            self.need_update = True
            stations = []

        for data in stations:
            item = CollectionData(
                name=data.get("name", "").replace("\t", "").replace("\n", "").strip(),
                url=data.get("url", ""),
            )
            item.add_info(data.get("country"), data.get("countrycode"), str(data.get("bitrate", 0)), data.get("codec"))
            results.append(item)

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
