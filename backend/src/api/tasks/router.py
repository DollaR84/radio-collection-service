import logging

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, HTTPException, status

from application import dto

from workers import TaskManager

from .. import schemas


router = APIRouter(prefix="/tasks", route_class=DishkaRoute)


@router.get(
    "/",
    description="Method to get list of task names",
    status_code=status.HTTP_200_OK,
    response_model=list[str],
)
async def get_tasks(
        user: FromDishka[dto.AdminUser],
        manager: FromDishka[TaskManager],
) -> list[str]:
    try:
        return manager.get_all_tasks_names()
    except Exception as error:
        logging.error(error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error to get list of task names for user with id='{user.id}'",
        ) from error


@router.post(
    "/",
    description="Method to run task by name",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.TaskResponse,
)
async def run_task(
        user: FromDishka[dto.AdminUser],
        manager: FromDishka[TaskManager],
        task_data: schemas.TaskRequest,
) -> schemas.TaskResponse:
    try:
        job_id = await manager.execute_task(task_data.name)
        return schemas.TaskResponse(job_id=job_id)

    except Exception as error:
        logging.error(error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error to run task for user with id='{user.id}'",
        ) from error


@router.get(
    "/{job_id}/status",
    description="Method to get status of running task",
    status_code=status.HTTP_200_OK,
    response_model=schemas.TaskJobStatus,
)
async def get_job_status(
        user: FromDishka[dto.AdminUser],
        manager: FromDishka[TaskManager],
        job_id: str,
) -> schemas.TaskJobStatus:
    try:
        return schemas.TaskJobStatus(
            job_id=job_id,
            status=await manager.get_job_status(job_id),
        )
    except Exception as error:
        logging.error(error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error to get status of job with id='job_id' for user with id='{user.id}'",
        ) from error


@router.get(
    "/{job_id}/info",
    description="Method to get status of running task",
    status_code=status.HTTP_200_OK,
    response_model=schemas.TaskJobResult,
)
async def get_job_info(
        user: FromDishka[dto.AdminUser],
        manager: FromDishka[TaskManager],
        job_id: str,
) -> schemas.TaskJobResult:
    try:
        info = await manager.get_job_info(job_id)
        return schemas.TaskJobResult(**info.dict())
    except Exception as error:
        logging.error(error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error to get info of job with id='job_id' for user with id='{user.id}'",
        ) from error
