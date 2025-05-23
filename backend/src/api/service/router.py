from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from application.services import NoService


router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/",
    description="Method for root page stub",
    status_code=status.HTTP_200_OK,
)
async def index(reasigner: FromDishka[NoService]) -> JSONResponse:
    status_code = status.HTTP_200_OK
    response = {
        "status": "OK",
        "reason": await reasigner("To login, follow the link: '/auth'"),
    }

    return JSONResponse(content=response, status_code=status_code)


@router.get(
    "/health",
    description="Method for check health api backend",
    status_code=status.HTTP_200_OK,
)
async def health_check() -> JSONResponse:
    status_code = status.HTTP_200_OK
    response = {"status": "OK"}

    return JSONResponse(content=response, status_code=status_code)
