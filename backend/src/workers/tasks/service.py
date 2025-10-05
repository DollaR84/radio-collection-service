import logging
from typing import Any

from apscheduler.triggers.cron import CronTrigger

from application import dto
from application.interactors import GetUsers, GetCurrentAccessPermission, UpdateUserByID, GetStationsWithDoubleName
from application.types import UserAccessRights

from .base import BaseTask


class PermissionDefaultTask(BaseTask):
    trigger = CronTrigger(hour=3, minute=0, timezone="UTC")

    def __init__(
            self,
            get_users: GetUsers,
            get_current_permission: GetCurrentAccessPermission,
            updater: UpdateUserByID,
    ):
        self.get_users: GetUsers = get_users
        self.get_current_permission: GetCurrentAccessPermission = get_current_permission
        self.updater: UpdateUserByID = updater

    async def execute(self, ctx: dict[Any, Any]) -> None:
        logging.info("starting task: %s", self.__class__.__name__)

        users = await self.get_users(exclude_access_rights=[UserAccessRights.DEFAULT, UserAccessRights.OWNER])
        total = len(users)

        for current, user in enumerate(users, start=1):
            if user.is_admin or await self.get_current_permission(user.id):
                continue

            update_data = dto.UpdateUser(access_rights=UserAccessRights.DEFAULT)
            await self.updater(user.id, update_data)

            ctx["progress"] = {
                "done": current,
                "total": total,
                "percent": round((current / total) * 100, 2),
            }

        logging.info("task completed: %s", self.__class__.__name__)


class FixDoubleNameStationsTask(BaseTask):

    def __init__(
            self,
            get_stations: GetStationsWithDoubleName,
    ):
        self.get_stations: GetStationsWithDoubleName = get_stations

    async def execute(self, ctx: dict[Any, Any]) -> None:
        logging.info("starting task: %s", self.__class__.__name__)

        stations = await self.get_stations()
        total = len(stations)

        with open("/app/data/double_name.log", "w", encoding="utf-8") as file_log:
            for current, station in enumerate(stations, start=1):
                file_log.write(f"{station.name}: {station.url}\n")

                ctx["progress"] = {
                    "done": current,
                    "total": total,
                    "percent": round((current / total) * 100, 2),
                }

        logging.info("task completed: %s", self.__class__.__name__)
