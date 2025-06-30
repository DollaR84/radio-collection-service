from .file import CreateFileGateway, DeleteFileGateway, GetFileGateway, UpdateFileGateway
from .station import (
    CreateStationGateway,
    DeleteStationGateway,
    GetStationGateway,
    GetStationsUrlsGateway,
    UpdateStationGateway,
    CreateFavoriteGateway,
    DeleteFavoriteGateway,
    GetFavoriteGateway,
)

from .user import (
    CreateUserGateway,
    DeleteUserGateway,
    GetUserGateway,
    UpdateUserGateway,
    CreateAccessPermissionGateway,
    DeleteAccessPermissionGateway,
    GetAccessPermissionGateway,
    UpdateAccessPermissionGateway,
)


__all__ = [
    "CreateStationGateway",
    "DeleteStationGateway",
    "GetStationsUrlsGateway",
    "GetStationGateway",
    "UpdateStationGateway",

    "CreateFileGateway",
    "DeleteFileGateway",
    "GetFileGateway",
    "UpdateFileGateway",

    "CreateFavoriteGateway",
    "DeleteFavoriteGateway",
    "GetFavoriteGateway",

    "CreateAccessPermissionGateway",
    "DeleteAccessPermissionGateway",
    "GetAccessPermissionGateway",
    "UpdateAccessPermissionGateway",

    "CreateUserGateway",
    "DeleteUserGateway",
    "GetUserGateway",
    "UpdateUserGateway",
]
