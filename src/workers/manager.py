from typing import Any, Optional, Type

from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from arq.jobs import Job as ArqJob
from arq import ArqRedis

from .tasks import BaseTask


class TaskManager:

    def __init__(
            self,
            scheduler: Optional[AsyncIOScheduler] = None,
            redis_pool: Optional[ArqRedis] = None,
    ):
        self.scheduler = scheduler
        self.redis_pool = redis_pool

        self._scheduled_tasks: list[Job] = []
        self._on_demand_tasks: dict[str, Type[BaseTask]] = {}

    def setup_scheduler(self) -> None:
        for task_cls in BaseTask.get_all_tasks():
            if task_cls.trigger:
                self._scheduled_tasks.append(self._create_scheduled_job(task_cls))

    def _create_scheduled_job(self, task_cls: Type[BaseTask]) -> Job:
        if self.scheduler is None:
            raise ValueError("need scheduler to work tasks on the schedule")

        return self.scheduler.add_job(
            task_cls().execute,
            trigger=task_cls.trigger,
        )

    def register_adhoc_tasks(self) -> None:
        for task_cls in BaseTask.get_all_tasks():
            self._on_demand_tasks[task_cls.get_name()] = task_cls

    async def trigger_task(self, task_name: str, *args: Any, **kwargs: Any) -> str:
        if self.redis_pool is None:
            raise ValueError("need redis pool to work tasks on the demand")

        if task_name not in self._on_demand_tasks:
            raise ValueError(f"Task '{task_name}' not registered")

        job: Optional[ArqJob] = await self.redis_pool.enqueue_job(
            "execute_registered_task",
            task_name,
            *args,
            **kwargs,
        )

        if not job or not job.job_id:
            raise RuntimeError("Failed to enqueue job")
        return job.job_id

    def get_task(self, task_name: str) -> Type[BaseTask]:
        return self._on_demand_tasks[task_name]
