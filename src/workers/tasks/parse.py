from datetime import datetime, timedelta
from typing import Any

from dishka.integrations.arq import inject

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from application.dto import Station
from application.interactors import CreateStation, GetStationUrls
from application.services import CollectionParser

from .base import BaseTask


class BaseCollectionTask(BaseTask, is_abstract=True):

    @inject
    async def execute(  # pylint: disable=arguments-differ
            self,
            parser: CollectionParser,
            get_urls: GetStationUrls,
            creator: CreateStation,
            *args: Any,
            **kwargs: Any,
    ) -> None:
        collection = parser.get_collection(self.get_name())
        data = await collection.parse()

        exists_urls = await get_urls()
        data = [collection_item for collection_item in data if collection_item.url not in exists_urls]

        await creator([Station(**item.dict()) for item in data])


class RadioBrowserTask(BaseCollectionTask):
    order_id = 1
    trigger = IntervalTrigger(days=7, start_date=datetime.utcnow() + timedelta(minutes=5))


class InternetRadioStreamsTask(BaseCollectionTask):
    order_id = 2
    trigger = CronTrigger(day=1, hour=0, minute=0)


class Mp3RadioStationsTask(BaseCollectionTask):
    order_id = 3
    trigger = CronTrigger(day=1, hour=0, minute=0)
