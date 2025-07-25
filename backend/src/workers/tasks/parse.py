import logging
from typing import Any

from apscheduler.triggers.cron import CronTrigger

from application.dto import CollectionData, Station
from application.interactors import (
    CreateStations,
    GetStationUrls,
    GetM3uFilesForParse,
    GetPlsFilesForParse,
    UpdateFileLoadStatus,
)
from application.services.parsers import CollectionParser, M3UParser, PLSParser
from application.services.parsers.base import BaseParser

from .base import BaseTask


class BaseParserTask(BaseTask, is_abstract=True):
    parser: BaseParser
    get_all_urls: GetStationUrls
    creator: CreateStations

    def __init__(
            self,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
    ):
        self.get_all_urls: GetStationUrls = get_all_urls
        self.creator: CreateStations = creator

    async def _saving(self, ctx: dict[Any, Any], parse_data: list[list[CollectionData]]) -> None:
        exists_urls_to_parse_data: set[str] = set()
        exists_urls_to_db = await self.get_all_urls()
        total = len(parse_data)

        for index, batch in enumerate(parse_data, start=1):
            data = []
            for item in batch:
                if item.url not in exists_urls_to_db and item.url not in exists_urls_to_parse_data:
                    data.append(item)
                    exists_urls_to_parse_data.add(item.url)

            if not data:
                continue

            await self.creator([
                Station(
                    name=item.name,
                    url=item.url,
                    tags=item.info_data,
                ) for item in data
            ])
            ctx["progress"] = {"done": f"saving: {index}/{total}"}


class BaseCollectionTask(BaseParserTask, is_abstract=True):

    def __init__(
            self,
            parser: CollectionParser,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
    ):
        super().__init__(get_all_urls, creator)
        self.parser: CollectionParser = parser

    async def execute(self, ctx: dict[Any, Any]) -> None:
        logging.info("starting task: %s", self.__class__.__name__)

        collection = self.parser.get_collection(self.get_name(), parser=self.parser)
        parse_data = await collection.parse()
        ctx["progress"] = {"done": "parsing"}
        logging.info("parsing task finished")

        await self._saving(ctx, parse_data)
        logging.info("task completed: %s", self.__class__.__name__)


class RadioBrowserTask(BaseCollectionTask):
    order_id = 1
    trigger = CronTrigger(hour=0, minute=0, timezone="UTC")


class InternetRadioStreamsTask(BaseCollectionTask):
    order_id = 2
    trigger = CronTrigger(hour=1, minute=0, timezone="UTC")


class Mp3RadioStationsTask(BaseCollectionTask):
    order_id = 3
    trigger = CronTrigger(hour=2, minute=0, timezone="UTC")


class BasePlaylistTask(BaseParserTask, is_abstract=True):
    get_files: GetM3uFilesForParse | GetPlsFilesForParse
    update_status: UpdateFileLoadStatus

    async def execute(self, ctx: dict[Any, Any]) -> None:
        logging.info("starting task: %s", self.__class__.__name__)
        files = await self.get_files()

        for file in files:
            parse_data = self.parser.get_data_from_file(file.file_path_with_id)
            ctx["progress"] = {"done": f"parsing file '{file.filename}'"}

            await self._saving(ctx, parse_data)
            await self.update_status(file.id)

        logging.info("task completed: %s", self.__class__.__name__)


class M3uPlaylistTask(BasePlaylistTask):

    def __init__(
            self,
            parser: M3UParser,
            get_m3u_files: GetM3uFilesForParse,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
            update_status: UpdateFileLoadStatus,
    ):
        super().__init__(get_all_urls, creator)
        self.parser = parser
        self.get_files = get_m3u_files
        self.update_status = update_status


class PlsPlaylistTask(BasePlaylistTask):

    def __init__(
            self,
            parser: PLSParser,
            get_pls_files: GetPlsFilesForParse,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
            update_status: UpdateFileLoadStatus,
    ):
        super().__init__(get_all_urls, creator)
        self.parser = parser
        self.get_files = get_pls_files
        self.update_status = update_status
