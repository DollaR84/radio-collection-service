from typing import Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, status

from application import interactors
from application.types import StationStatusType

from .. import schemas


router = APIRouter(route_class=DishkaRoute)


@router.get(
    "/stations",
    description="Method for get list radio stations",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.StationResponse],
)
async def get_stations(
        interactor: FromDishka[interactors.GetStations],
        name: Optional[str] = None,
        info: Optional[str] = None,
        status_type: Optional[StationStatusType] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
) -> list[schemas.StationResponse]:
    stations = await interactor(name, info, status_type, offset, limit)
    return [
        schemas.StationResponse(**station.dict())
        for station in stations
    ]
