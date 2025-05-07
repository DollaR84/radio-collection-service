from typing import Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, HTTPException, status

from application import dto
from application import interactors
from application.types import StationStatusType

from .. import schemas


router = APIRouter(prefix="/stations", route_class=DishkaRoute)


@router.get(
    "/",
    description="Method for get list radio stations",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.StationResponse],
)
async def get_stations(
        user: FromDishka[dto.CurrentUser],
        interactor: FromDishka[interactors.GetStations],
        name: Optional[str] = None,
        info: Optional[str] = None,
        status_type: Optional[StationStatusType] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
) -> list[schemas.StationResponse]:
    stations = await interactor(user, name, info, status_type, offset, limit)
    return [
        schemas.StationResponse(**station.dict())
        for station in stations
    ]


@router.get(
    "/{station_id}",
    description="Method for get radio station by id",
    status_code=status.HTTP_200_OK,
    response_model=schemas.StationResponse,
)
async def get_station(
        user: FromDishka[dto.CurrentUser],
        interactor: FromDishka[interactors.GetStation],
        station_id: int,
) -> schemas.StationResponse:
    station = await interactor(user, station_id)
    if station is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"radio station with id={station_id} not found",
        )

    return schemas.StationResponse(**station.dict())
