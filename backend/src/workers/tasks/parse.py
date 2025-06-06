from datetime import datetime, timedelta
import logging

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from application.dto import Station
from application.interactors import CreateStation, GetStationUrls
from application.services import CollectionParser

from .base import BaseTask


class BaseCollectionTask(BaseTask, is_abstract=True):
    parser: CollectionParser
    get_all_urls: GetStationUrls
    creator: CreateStation

    def __init__(
            self,
            parser: CollectionParser,
            get_all_urls: GetStationUrls,
            creator: CreateStation,
    ):
        self.parser: CollectionParser = parser
        self.get_all_urls: GetStationUrls = get_all_urls
        self.creator: CreateStation = creator

    async def execute(self) -> None:
        logging.info("starting task: %s", self.__class__.__name__)

        collection = self.parser.get_collection(self.get_name(), parser=self.parser)
        parse_data = await collection.parse()

        exists_urls_to_parse_data: set[str] = set()
        exists_urls_to_db = await self.get_all_urls()
        for chunk_data in parse_data:
            data = []
            for item in chunk_data:
                if item.url not in exists_urls_to_db and not exists_urls_to_parse_data:
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
