import logging
import os
import shutil
from typing import Optional

from config import Config

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, HTTPException, status, File, UploadFile

from application import dto
from application import interactors
from application.services import Uploader
from application.types import StationStatusType

from .. import schemas


router = APIRouter(prefix="/stations", route_class=DishkaRoute)


@router.get(
    "/",
    description="Method for get list radio stations",
    status_code=status.HTTP_200_OK,
    response_model=schemas.StationsResponse,
)
async def get_stations(
        user: FromDishka[dto.CurrentUser],
        interactor: FromDishka[interactors.GetStationsWithCount],
        name: Optional[str] = None,
        info: Optional[str] = None,
        status_type: Optional[StationStatusType] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
) -> schemas.StationsResponse:
    try:
        data = await interactor(name, info, status_type, offset, limit)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"error get radio stations for user id={user.id}",
        ) from error

    stations = [
        schemas.StationResponse(**station.dict())
        for station in data.stations
    ]

    return schemas.StationsResponse(items=stations, total=data.count)


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
    station = await interactor(station_id)
    if station is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"radio station with id={station_id} for user id={user.id} not found",
        )

    return schemas.StationResponse(**station.dict())


@router.post(
    "/",
    description="Method for send radio station on server",
    status_code=status.HTTP_200_OK,
    response_model=schemas.StationsSavingResponse,
)
async def send_station(
        user: FromDishka[dto.PlusUser],
        uploader: FromDishka[Uploader],
        data: schemas.StationRequest,
) -> schemas.StationsSavingResponse:
    logging.info("user %d '%s' send station", user.id, user.user_name)

    station = dto.Station(**data.dict())
    uploader.load(station)

    saving_count = await uploader.process()
    return schemas.StationsSavingResponse(count=saving_count)


@router.post(
    "/list",
    description="Method for send radio stations on server",
    status_code=status.HTTP_200_OK,
    response_model=schemas.StationsSavingResponse,
)
async def send_stations(
        user: FromDishka[dto.PlusUser],
        uploader: FromDishka[Uploader],
        data: schemas.StationsRequest,
) -> schemas.StationsSavingResponse:
    logging.info("user %d '%s' send stations", user.id, user.user_name)

    stations = [dto.Station(**item.dict()) for item in data.items]
    uploader.load(dto.Stations(items=stations))

    saving_count = await uploader.process()
    return schemas.StationsSavingResponse(count=saving_count)


@router.post(
    "/playlist",
    description="Method for send radio stations playlist (m3u, pls) on server",
    status_code=status.HTTP_200_OK,
    response_model=schemas.StationsSavingResponse,
)
async def send_playlist(
        user: FromDishka[dto.PlusUser],
        uploader: FromDishka[Uploader],
        config: FromDishka[Config],
        file: UploadFile = File(...),
) -> schemas.StationsSavingResponse:
    if file.filename is None:
        raise ValueError(f"file '{file}' has not filename")

    file_path = os.path.join(config.api.upload_folder, file.filename)
    logging.info("user %d '%s' send playlist '%s'", user.id, user.user_name, file_path)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if file.filename.lower().endswith(".m3u"):
        uploader.load(dto.UploadM3UFile(filename=file_path))
    elif file.filename.lower().endswith(".pls"):
        uploader.load(dto.UploadPLSFile(filename=file_path))
    else:
        raise ValueError("unsupported file format extension")

    saving_count = await uploader.process()
    return schemas.StationsSavingResponse(count=saving_count)
