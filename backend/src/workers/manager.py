from typing import Any, Optional, Type

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from arq import ArqRedis
from arq.connections import RedisSettings, create_pool
from arq.jobs import Job as ArqJob

from config import Config

from dishka import AsyncContainer

from .exceptions import SchedulerNotInitializedError, ContainerNotInitializedError
from .tasks import BaseTask


class TaskManager:

    def __init__(self) -> None:
        self.redis_pool: Optional[ArqRedis] = None

        self._scheduled_tasks: list[Job] = []
        self._on_demand_tasks: dict[str, Type[BaseTask]] = {}
        self._arq_context: dict[Any, Any] = {}

    @property
    def arq_context(self) -> dict[Any, Any]:
        return self._arq_context

    @arq_context.setter
    def arq_context(self, context: dict[Any, Any]) -> None:
        context["task_manager"] = self
        self._arq_context = context

    @property
    def redis(self) -> Optional[ArqRedis]:
        return self._arq_context.get("redis") or self.redis_pool

    @property
    def scheduler(self) -> Optional[AsyncIOScheduler]:
        return self._arq_context.get("scheduler")

    @scheduler.setter
    def scheduler(self, scheduler: AsyncIOScheduler) -> None:
        self._arq_context["scheduler"] = scheduler

    @property
    def dishka_container(self) -> Optional[AsyncContainer]:
        return self._arq_context.get("dishka_container")

    @dishka_container.setter
    def dishka_container(self, container: AsyncContainer) -> None:
        self._arq_context["dishka_container"] = container

    async def create_redis_pool(self, config: Config) -> None:
        self.redis_pool = await create_pool(RedisSettings(
            host=config.redis.host,
            port=config.redis.port,
            database=config.worker.redis_database,
        ))

    @staticmethod
    def get_all_tasks_names() -> list[str]:
        return BaseTask.get_all_tasks_names()

    def register_adhoc_tasks(self) -> None:
        for task_cls in BaseTask.get_all_tasks():
            self._on_demand_tasks[task_cls.get_name()] = task_cls

    def setup_scheduler(self) -> None:
        for task_cls in BaseTask.get_all_tasks():
            self._on_demand_tasks[task_cls.get_name()] = task_cls
            if task_cls.trigger:
                self._scheduled_tasks.append(self._create_scheduled_job(task_cls))

    def _create_scheduled_job(self, task_cls: Type[BaseTask]) -> Job:
        if self.scheduler is None:
            raise SchedulerNotInitializedError()

        return self.scheduler.add_job(
            self.execute_task,
            trigger=task_cls.trigger,
            args=[task_cls.get_name()],
        )

    async def execute_task(self, task_name: str) -> str:
        if self.redis is None:
            raise ValueError("need redis pool to work tasks")

        if task_name not in self._on_demand_tasks:
            raise ValueError(f"Task '{task_name}' not registered")

        job: Optional[ArqJob] = await self.redis.enqueue_job(
            "execute_register_task",
            task_name,
        )

        if not job or not job.job_id:
            raise RuntimeError("Failed to enqueue job")
        return job.job_id

    async def get_task(self, task_name: str) -> BaseTask:
        if self.dishka_container is None:
            raise ContainerNotInitializedError()

        task_cls = self._on_demand_tasks[task_name]
        async with self.dishka_container() as container:
            task = await container.get(task_cls)
            return task
