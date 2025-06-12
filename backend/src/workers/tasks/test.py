import asyncio
from datetime import datetime, timedelta
import logging
from typing import Any, Optional

from apscheduler.triggers.interval import IntervalTrigger

from application import dto
from application.interactors import GetStations, UpdateStationsStatus
from application.services import RadioTestData, RadioTester
from application.types import StationStatusType

from .base import BaseTask


class BaseTestTask(BaseTask, is_abstract=True):
    tester: RadioTester
    get_stations: GetStations
    updater: UpdateStationsStatus

    def __init__(
            self,
            tester: RadioTester,
            get_stations: GetStations,
            updater: UpdateStationsStatus,
    ):
        self.tester: RadioTester = tester
        self.get_stations: GetStations = get_stations
        self.updater: UpdateStationsStatus = updater

        self.results_queue: asyncio.Queue[Optional[dto.UpdateStationStatus]] = asyncio.Queue()
        self._stop_processing = False

    async def process_results_queue(self) -> None:
        batch = []
        while not self._stop_processing or not self.results_queue.empty():
            try:
                result = await asyncio.wait_for(self.results_queue.get(), timeout=self.tester.config.queue_timeout)
                if result is None:
                    continue
                batch.append(result)
                if len(batch) >= self.tester.config.batch_size or (self._stop_processing and batch):
                    try:
                        await self.updater(batch)
                        batch.clear()
                    except Exception as error:
                        logging.error("failed to update batch: %s", str(error))
                    await asyncio.sleep(self.tester.config.update_timeout)
            except asyncio.TimeoutError:
                continue
            except Exception as error:
                logging.error("error in results processor: %s", str(error))

    async def check(self, ctx: dict[Any, Any], stations: list[dto.StationData]) -> None:
        total = len(stations)
        processor_task = asyncio.create_task(self.process_results_queue())

        try:
            async def limited_check(station: dto.StationData) -> None:
                await self.tester.check(station.id, station.url, self.callback)
                current = ctx.get("_checked", 0) + 1
                ctx["_checked"] = current

                if current % 20 == 0 or current == total:
                    ctx["progress"] = {
                        "done": current,
                        "total": total,
                        "percent": round((current / total) * 100, 2),
                    }

            await asyncio.gather(*[
                limited_check(station)
                for station in stations
            ])

        finally:
            self._stop_processing = True
            await self.results_queue.put(None)
            await processor_task

    async def callback(self, data: RadioTestData) -> None:
        update_data = dto.UpdateStationStatus(
            id=data.id,
            status=StationStatusType.WORKS if data.is_success else StationStatusType.NOT_WORK,
        )
        await self.results_queue.put(update_data)

    async def process(self, ctx: dict[Any, Any], stations: list[dto.StationData]) -> None:
        logging.info("starting task: %s", self.__class__.__name__)

        self._stop_processing = False
        try:
            await self.check(ctx, stations)
        finally:
            self._stop_processing = True
            while not self.results_queue.empty():
                await asyncio.sleep(self.tester.config.update_timeout)

        logging.info("task completed: %s", self.__class__.__name__)


class TestNotVerifiedTask(BaseTestTask):
    trigger = IntervalTrigger(hours=2, start_date=datetime.utcnow() + timedelta(minutes=30))

    async def execute(self, ctx: dict[Any, Any]) -> None:
        stations = await self.get_stations(
            status=StationStatusType.NOT_VERIFIED,
            limit=self.tester.config.batch_limit,
        )
        await self.process(ctx, stations)


class TestNotWorkTask(BaseTestTask):
    trigger = IntervalTrigger(hours=5, start_date=datetime.utcnow() + timedelta(hours=1))

    async def execute(self, ctx: dict[Any, Any]) -> None:
        stations = await self.get_stations(
            status=StationStatusType.NOT_WORK,
            limit=self.tester.config.batch_limit,
        )
        await self.process(ctx, stations)


class TestWorksTask(BaseTestTask):
    trigger = IntervalTrigger(days=1, start_date=datetime.utcnow() + timedelta(hours=1, minutes=45))

    async def execute(self, ctx: dict[Any, Any]) -> None:
        stations = await self.get_stations(
            status=StationStatusType.WORKS,
            limit=self.tester.config.batch_limit,
        )
        await self.process(ctx, stations)
