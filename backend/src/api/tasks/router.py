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
            detail=f"error to get list of task names for user with id={user.id}",
        ) from error


@router.post(
    "/",
    description="Method to run task by name",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.TaskStartedResponse,
)
async def run_task(
        user: FromDishka[dto.AdminUser],
        manager: FromDishka[TaskManager],
        task_data: schemas.TaskData,
) -> schemas.TaskStartedResponse:
    try:
        job_id = await manager.execute_task(task_data.name)
        return schemas.TaskStartedResponse(job_id=job_id)

    except Exception as error:
        logging.error(error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error to run task for user with id={user.id}",
        ) from error
