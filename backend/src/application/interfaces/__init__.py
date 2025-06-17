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

from .user import (
    CreateUserInterface,
    DeleteUserInterface,
    GetUserInterface,
    UpdateUserInterface,
    CreateAccessPermissionInterface,
    DeleteAccessPermissionInterface,
    GetAccessPermissionInterface,
    UpdateAccessPermissionInterface,
)


__all__ = [
    "CreateStationInterface",
    "DeleteStationInterface",
    "GetStationsUrlsInterface",
    "GetStationInterface",
    "UpdateStationInterface",

    "CreateFavoriteInterface",
    "DeleteFavoriteInterface",
    "GetFavoriteInterface",

    "CreateAccessPermissionInterface",
    "DeleteAccessPermissionInterface",
    "GetAccessPermissionInterface",
    "UpdateAccessPermissionInterface",

    "CreateUserInterface",
    "DeleteUserInterface",
    "GetUserInterface",
    "UpdateUserInterface",
]
