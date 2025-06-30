from .file import CreateFileInterface, DeleteFileInterface, GetFileInterface, UpdateFileInterface
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
    "CreateFileInterface",
    "GetFileInterface",
    "DeleteFileInterface",
    "UpdateFileInterface",

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
