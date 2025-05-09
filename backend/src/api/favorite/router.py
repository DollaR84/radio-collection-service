from typing import Optional

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from application import dto
from application import interactors

from .. import schemas


router = APIRouter(prefix="/favorites", route_class=DishkaRoute)


@router.get(
    "/",
    description="Method for get list favorites radio stations",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.StationResponse],
)
async def get_favorites(
        user: FromDishka[dto.CurrentUser],
        interactor: FromDishka[interactors.GetUserFavorites],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
) -> list[schemas.StationResponse]:
    stations = await interactor(user.id, offset, limit)
    return [
        schemas.StationResponse(**station.dict())
        for station in stations
    ]


@router.post(
    "/",
    description="Method for add radio station to user favorites",
    status_code=status.HTTP_201_CREATED,
)
async def add_favorites(
        user: FromDishka[dto.CurrentUser],
        interactor: FromDishka[interactors.CreateFavorite],
        data: schemas.AddFavorite,
) -> JSONResponse:
    favorite_id = await interactor(user.id, data.station_id)
    if favorite_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error creating favorite radio station with id={data.station_id}",
        )

    status_code = status.HTTP_201_CREATED
    response = {"status": "OK"}

    return JSONResponse(content=response, status_code=status_code)


@router.delete(
    "/{station_id}",
    description="Method for delete radio station from user favorites",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_favorites(
        user: FromDishka[dto.CurrentUser],
        interactor: FromDishka[interactors.DeleteFavorite],
        station_id: int,
) -> JSONResponse:
    try:
        await interactor(user.id, station_id)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"favorite radio station with id={station_id} for user id={user.id} not found",
        ) from error

    status_code = status.HTTP_204_NO_CONTENT
    response = {"status": "OK"}

    return JSONResponse(content=response, status_code=status_code)
