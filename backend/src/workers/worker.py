import asyncio
import logging
from typing import Any, cast, Type

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from arq.connections import RedisSettings
from arq.cron import CronJob
from arq.typing import WorkerCoroutine, WorkerSettingsBase
from arq.worker import create_worker

from config import Config, get_config

from container import setup_container

from .context import ArqContext
from .exceptions import TaskManagerNotInitializedError
from .manager import TaskManager


async def execute_register_task(ctx: dict[Any, Any], task_name: str) -> Any:
    _ctx = cast(ArqContext, ctx)
    if _ctx.task_manager is None:
        raise TaskManagerNotInitializedError()

    task_cls = _ctx.task_manager.get_task(task_name)
    await _ctx.task_manager.execute_task(task_cls)


def get_worker_settings(config: Config) -> Type[WorkerSettingsBase]:
    async def on_startup(ctx: dict[Any, Any]) -> dict[Any, Any]:
        _ctx = ArqContext(ctx)
        setup_container(_ctx, config)

        _ctx.scheduler = AsyncIOScheduler()
        _ctx.task_manager = TaskManager(scheduler=_ctx.scheduler, container=_ctx.dishka_container)
        _ctx.task_manager.setup_scheduler()
        _ctx.scheduler.start()

        return _ctx

    async def on_shutdown(ctx: dict[Any, Any]) -> Any:
        _ctx = cast(ArqContext, ctx)
        await _ctx.dishka_container.close()
        if _ctx.scheduler:
            await _ctx.scheduler.shutdown()

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

        on_startup = on_startup
        on_shutdown = on_shutdown

    return WorkerSettings


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s  %(process)-7s %(module)-20s %(message)s',
    )

    config: Config = get_config()
    worker = create_worker(get_worker_settings(config))
    asyncio.run(worker.async_run())


if "__main__" == __name__:
    main()
