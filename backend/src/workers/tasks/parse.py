from datetime import datetime, timedelta
import logging
from typing import Any

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from application.dto import Station
from application.interactors import CreateStations, GetStationUrls
from application.services import CollectionParser

from .base import BaseTask


class BaseCollectionTask(BaseTask, is_abstract=True):
    parser: CollectionParser
    get_all_urls: GetStationUrls
    creator: CreateStations

    def __init__(
            self,
            parser: CollectionParser,
            get_all_urls: GetStationUrls,
            creator: CreateStations,
    ):
        self.parser: CollectionParser = parser
        self.get_all_urls: GetStationUrls = get_all_urls
        self.creator: CreateStations = creator

    async def execute(self, ctx: dict[Any, Any]) -> None:
        logging.info("starting task: %s", self.__class__.__name__)

        collection = self.parser.get_collection(self.get_name(), parser=self.parser)
        parse_data = await collection.parse()
        ctx["progress"] = {"done": "parsing"}

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

        logging.info("task completed: %s", self.__class__.__name__)


class RadioBrowserTask(BaseCollectionTask):
    order_id = 1
    trigger = IntervalTrigger(days=7, start_date=datetime.utcnow() + timedelta(hours=1))


class InternetRadioStreamsTask(BaseCollectionTask):
    order_id = 2
    trigger = CronTrigger(day=1, hour=0, minute=0)


class Mp3RadioStationsTask(BaseCollectionTask):
    order_id = 3
    trigger = CronTrigger(day=1, hour=0, minute=0)
