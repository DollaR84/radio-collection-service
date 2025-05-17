from datetime import datetime, timedelta

from dishka import FromDishka
from dishka.integrations.arq import inject

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

    @inject
    async def initialize(
            self,
            parser: FromDishka[CollectionParser],
            get_all_urls: FromDishka[GetStationUrls],
            creator: FromDishka[CreateStation],
    ) -> None:
        self.parser: CollectionParser = parser
        self.get_all_urls: GetStationUrls = get_all_urls
        self.creator: CreateStation = creator

    async def execute(self) -> None:
        collection = self.parser.get_collection(self.get_name())
        data = await collection.parse()

        exists_urls = await self.get_all_urls()
        data = [collection_item for collection_item in data if collection_item.url not in exists_urls]

        await self.creator([Station(**item.dict()) for item in data])


class RadioBrowserTask(BaseCollectionTask):
    order_id = 1
    trigger = IntervalTrigger(days=7, start_date=datetime.utcnow() + timedelta(hours=1))


class InternetRadioStreamsTask(BaseCollectionTask):
    order_id = 2
    trigger = CronTrigger(day=1, hour=0, minute=0)


class Mp3RadioStationsTask(BaseCollectionTask):
    order_id = 3
    trigger = CronTrigger(day=1, hour=0, minute=0)
