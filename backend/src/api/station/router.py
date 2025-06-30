import logging
from typing import Optional

from config import Config

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from fastapi import APIRouter, HTTPException, status, File, UploadFile

from application import dto
from application import interactors
from application.services import Uploader
from application.types import StationStatusType, FilePlaylistType

from workers import TaskManager

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
    response_model=schemas.PlaylistSavingResponse,
)
async def send_station(
        user: FromDishka[dto.PlusUser],
        uploader: FromDishka[Uploader],
        config: FromDishka[Config],
        manager: FromDishka[TaskManager],
        data: schemas.StationRequest,
) -> schemas.PlaylistSavingResponse:
    logging.info("user %d '%s' send station", user.id, user.user_name)

    station = dto.Station(**data.dict())
    new_file = uploader.load(dto.UploadStation(user_id=user.id, file_path=config.api.upload_folder, station=station))
    await uploader.process(new_file)

    try:
        task_name = "M3u Playlist" if new_file.fileext == FilePlaylistType.M3U.value else "Pls Playlist"
        job_id = await manager.execute_task(task_name)
        return schemas.PlaylistSavingResponse(ok=True, message="station saving...", job_id=job_id)

    except Exception as error:
        logging.error(error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"error to run task parsing station for user with id='{user.id}'",
        ) from error


@router.post(
    "/list",
    description="Method for send radio stations on server",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PlaylistSavingResponse,
)
async def send_stations(
        user: FromDishka[dto.PlusUser],
        uploader: FromDishka[Uploader],
        config: FromDishka[Config],
        manager: FromDishka[TaskManager],
        data: schemas.StationsRequest,
) -> schemas.PlaylistSavingResponse:
    logging.info("user %d '%s' send stations", user.id, user.user_name)

    stations = [dto.Station(**item.dict()) for item in data.items]
    new_file = uploader.load(
        dto.UploadStations(user_id=user.id, file_path=config.api.upload_folder, stations=stations)
    )
    await uploader.process(new_file)

    try:
        task_name = "M3u Playlist" if new_file.fileext == FilePlaylistType.M3U.value else "Pls Playlist"
        job_id = await manager.execute_task(task_name)
        return schemas.PlaylistSavingResponse(ok=True, message="stations saving...", job_id=job_id)

    except Exception as error:
        logging.error(error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"error to run task parsing stations for user with id='{user.id}'",
        ) from error


@router.post(
    "/playlist",
    description="Method for send radio stations playlist (m3u, pls) on server",
    status_code=status.HTTP_200_OK,
    response_model=schemas.PlaylistSavingResponse,
)
async def send_playlist(
        user: FromDishka[dto.PlusUser],
        uploader: FromDishka[Uploader],
        config: FromDishka[Config],
        manager: FromDishka[TaskManager],
        file: UploadFile = File(...),
) -> schemas.PlaylistSavingResponse:
    if file.filename is None:
        raise ValueError(f"file '{file}' has not filename")

    new_file = uploader.load(dto.UploadPlaylist(user_id=user.id, file_path=config.api.upload_folder, file=file))
    await uploader.process(new_file)
    logging.info("user %d '%s' send playlist '%s'", user.id, user.user_name, new_file.filename)

    try:
        task_name = "M3u Playlist" if new_file.fileext == FilePlaylistType.M3U.value else "Pls Playlist"
        job_id = await manager.execute_task(task_name)
        return schemas.PlaylistSavingResponse(ok=True, message="playlist saving...", job_id=job_id)

    except Exception as error:
        logging.error(error, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"error to run task parsing playlist for user with id='{user.id}'",
        ) from error
