from functools import singledispatchmethod
import logging
from typing import Optional

from application import dto
from application import interactors

from config import ParserConfig

from fastapi import UploadFile

from .parsers import M3UParser, PLSParser


class Uploader:

    def __init__(
            self,
            config: ParserConfig,
            get_all_urls: interactors.GetStationUrls,
            creator: interactors.CreateStations,
    ):
        self.config = config
        self.get_all_urls = get_all_urls
        self.creator = creator

        self.items: list[dto.CollectionData] = []

    def add(self, name: str, url: str, tags: Optional[list[str]] = None) -> None:
        item = dto.CollectionData(name=name, url=url)

        if tags:
            item.add_info(*tags)

        self.items.append(item)

    def _parse(self, filename: str, parser: M3UParser | PLSParser) -> None:
        data = parser.get_data_from_file(filename)
        self.items.extend(data)

    @singledispatchmethod
    def load(self, data: dto.Station | dto.Stations | dto.UploadM3UFile | dto.UploadPLSFile) -> None:
        raise NotImplementedError("Cannot load station data")

    @load.register
    def _(self, data: dto.Station) -> None:
        self.add(data.name, data.url, data.tags)

    @load.register
    def _(self, data: dto.Stations) -> None:
        for item in data.items:
            self.add(item.name, item.url, item.tags)

    @load.register
    def _(self, data: dto.UploadM3UFile) -> None:
        self._parse(data.filename, M3UParser(self.config))

    @load.register
    def _(self, data: dto.UploadPLSFile) -> None:
        self._parse(data.filename, PLSParser(self.config))

    @property
    def batch_items(self) -> list[list[dto.CollectionData]]:
        data = []
        batch: list[dto.CollectionData] = []

        for item in self.items:
            if len(batch) >= self.config.batch_size:
                data.append(batch)
                batch = []

            batch.append(item)
        data.append(batch)

        return data

    async def process(self) -> int:
        exists_urls_in_parse_data: set[str] = set()
        exists_urls_in_db = await self.get_all_urls()
        total = len(self.items)
        saving_count = 0

        for index, batch in enumerate(self.batch_items, start=1):
            data = []
            for item in batch:
                if item.url not in exists_urls_in_db and item.url not in exists_urls_in_parse_data:
                    data.append(item)
                    exists_urls_in_parse_data.add(item.url)

            if not data:
                continue

            await self.creator([
                dto.Station(
                    name=item.name,
                    url=item.url,
                    tags=item.info_data,
                ) for item in data
            ])

            count = len(data)
            saving_count += count
            logging.info("saving %d batch part: %d stations from %d", index, count, total)

        return saving_count
