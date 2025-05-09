from .create import CreateStationInterface, CreateFavoriteInterface
from .delete import DeleteStationInterface, DeleteFavoriteInterface
from .read import GetStationInterface, GetStationsUrlsInterface, GetFavoriteInterface


__all__ = [
    "CreateStationInterface",
    "DeleteStationInterface",
    "GetStationInterface",
    "GetStationsUrlsInterface",

    "CreateFavoriteInterface",
    "DeleteFavoriteInterface",
    "GetFavoriteInterface",
]
