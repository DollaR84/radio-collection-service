import asyncio
from datetime import datetime, timedelta
import logging

from dishka import FromDishka
from dishka.integrations.arq import inject

from apscheduler.triggers.interval import IntervalTrigger

from application import dto
from application.interactors import GetStations, UpdateStationStatus
from application.services import RadioTestData, RadioTester
from application.types import StationStatusType

from .base import BaseTask


class BaseTestTask(BaseTask, is_abstract=True):
    tester: RadioTester
    get_stations: GetStations
    updater: UpdateStationStatus

    @inject
    async def initialize(
            self,
            tester: FromDishka[RadioTester],
            get_stations: FromDishka[GetStations],
            updater: FromDishka[UpdateStationStatus],
    ) -> None:
        self.tester: RadioTester = tester
        self.get_stations: GetStations = get_stations
        self.updater: UpdateStationStatus = updater

    async def check(self, stations: list[dto.StationData]) -> None:
        await asyncio.gather(*[
            self.tester.check(station.id, station.url, self.callback)
            for station in stations
        ])

    async def callback(self, data: RadioTestData) -> None:
        update_data = dto.UpdateStationStatus(
            id=data.id,
            status=StationStatusType.WORKS if data.is_success else StationStatusType.NOT_WORK,
        )
        await self.updater(update_data)


class TestNotVerifiedTask(BaseTestTask):
    trigger = IntervalTrigger(days=1, start_date=datetime.utcnow() + timedelta(hours=2))

    async def execute(self) -> None:
        logging.info("starting task: %s", self.__class__.__name__)

        stations = await self.get_stations(status=StationStatusType.NOT_VERIFIED)
        await self.check(stations)

        logging.info("task completed: %s", self.__class__.__name__)


class TestNotWorkTask(BaseTestTask):
    trigger = IntervalTrigger(days=3, start_date=datetime.utcnow() + timedelta(hours=3))

    async def execute(self) -> None:
        logging.info("starting task: %s", self.__class__.__name__)

        stations = await self.get_stations(status=StationStatusType.NOT_WORK)
        await self.check(stations)

        logging.info("task completed: %s", self.__class__.__name__)
