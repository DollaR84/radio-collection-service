from .station import (
    CreateStationInterface,
    DeleteStationInterface,
    GetStationInterface,
    GetStationsUrlsInterface,
    UpdateStationInterface,
    CreateFavoriteInterface,
    DeleteFavoriteInterface,
    GetFavoriteInterface,
)

from .user import CreateUserInterface, DeleteUserInterface, GetUserInterface, UpdateUserInterface


__all__ = [
    "CreateStationInterface",
    "DeleteStationInterface",
    "GetStationsUrlsInterface",
    "GetStationInterface",
    "UpdateStationInterface",

    "CreateFavoriteInterface",
    "DeleteFavoriteInterface",
    "GetFavoriteInterface",

    "CreateUserInterface",
    "DeleteUserInterface",
    "GetUserInterface",
    "UpdateUserInterface",
]
