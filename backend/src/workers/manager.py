from typing import Any, Optional, Type

from apscheduler.job import Job as schedulerJob
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from arq import ArqRedis
from arq.connections import RedisSettings, create_pool
from arq.jobs import JobDef, JobStatus, JobResult
from arq.jobs import Job as ArqJob

from application import dto

from config import Config

from dishka import AsyncContainer

from redis.connection import parse_url

from .exceptions import SchedulerNotInitializedError, ContainerNotInitializedError, RedisPoolNotInitializedError
from .tasks import BaseTask


class TaskManager:

    def __init__(self) -> None:
        self.redis_pool: Optional[ArqRedis] = None

        self._scheduled_tasks: list[schedulerJob] = []
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
        parsed_params = parse_url(config.redis.url) if config.redis.url else {}

        self.redis_pool = await create_pool(RedisSettings(
            host=parsed_params.get("host", config.redis.host),
            port=parsed_params.get("port", config.redis.port),
            password=parsed_params.get("password", None),
            database=parsed_params.get("db", config.worker.redis_database),
        ))

    async def close(self) -> None:
        if self.redis_pool:
            await self.redis_pool.close()

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

    def _create_scheduled_job(self, task_cls: Type[BaseTask]) -> schedulerJob:
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

    def get_job(self, job_id: str) -> ArqJob:
        if self.redis is None:
            raise RedisPoolNotInitializedError()

        return ArqJob(job_id, redis=self.redis)

    async def get_job_status(self, job_id: str) -> str:
        job = self.get_job(job_id)
        status = await job.status()
        return status.name

    async def get_job_info(self, job_id: str) -> dto.JobResult:
        job = self.get_job(job_id)
        info: Optional[JobDef] = await job.info()
        if info is None:
            raise ValueError(f"job result for for job_id: '{job_id}' not found")

        status: JobStatus = await job.status()
        result_info: Optional[JobResult] = await job.result_info()

        progress = None
        if status == JobStatus.in_progress:
            try:
                progress_data = await job.result(timeout=0.1, poll_delay=0)
                if isinstance(progress_data, dict) and "progress" in progress_data:
                    progress = progress_data["progress"]
            except Exception:
                pass

        result = None
        success = status == JobStatus.complete
        if success and result_info and result_info.result is None:
            try:
                result = await job.result(timeout=0.1)
            except Exception as error:
                result = str(error)

        return dto.JobResult(
            job_id=job_id,
            task_name=info.args[0] if info.args and len(info.args) > 0 else "unknown",
            success=success,
            job_try=result_info.job_try if result_info else 0,
            start_time=result_info.start_time if result_info else None,
            finish_time=result_info.finish_time if result_info else None,
            enqueue_time=info.enqueue_time,
            score=info.score,
            result=result,
            progress=progress,
        )
