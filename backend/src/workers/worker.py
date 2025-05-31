import asyncio
import logging
from typing import Any, Optional, Type

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from arq.connections import RedisSettings
from arq.cron import CronJob
from arq.typing import WorkerCoroutine, WorkerSettingsBase
from arq.worker import create_worker

from config import Config, get_config

from container import setup_container

from .exceptions import TaskManagerNotInitializedError
from .manager import TaskManager


async def execute_register_task(ctx: dict[Any, Any], task_name: str) -> Any:
    task_manager = ctx.get("task_manager")
    if task_manager is None:
        raise TaskManagerNotInitializedError()

    task = await task_manager.get_task(task_name)
    try:
        await task.execute()
    except Exception as error:
        logging.error("task '%s' failed: %s", task.get_name(), str(error))


def get_worker_settings(config: Config, loop: Optional[asyncio.AbstractEventLoop] = None) -> Type[WorkerSettingsBase]:
    class WorkerSettings(WorkerSettingsBase):
        redis_settings = RedisSettings(
            host=config.redis.host,
            port=config.redis.port,
            database=config.worker.redis_database,
        )
        handle_signals: bool = config.worker.handle_signals

        health_check_interval: int = config.worker.health_check_interval
        max_jobs: int = config.worker.max_jobs
        job_timeout: int = config.worker.job_timeout

        functions: list[WorkerCoroutine] = [execute_register_task]
        cron_jobs: list[CronJob] = []

        @staticmethod
        async def on_startup(ctx: dict[Any, Any]) -> dict[Any, Any]:
            task_manager = TaskManager()
            task_manager.arq_context = ctx
            setup_container(task_manager, config)

            task_manager.scheduler = AsyncIOScheduler(event_loop=loop or asyncio.get_event_loop())
            task_manager.setup_scheduler()
            task_manager.scheduler.start()

            return task_manager.arq_context

        @staticmethod
        async def on_shutdown(ctx: dict[Any, Any]) -> Any:
            task_manager = ctx.get("task_manager")
            if task_manager is None:
                raise TaskManagerNotInitializedError()

            if task_manager.dishka_container:
                await task_manager.dishka_container.close()

            if task_manager.scheduler:
                await task_manager.scheduler.shutdown()

    return WorkerSettings


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s  %(process)-7s %(module)-20s %(message)s',
    )
    config: Config = get_config()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        worker = create_worker(get_worker_settings(config, loop))
        loop.run_until_complete(worker.async_run())
    finally:
        loop.close()


if "__main__" == __name__:
    main()
