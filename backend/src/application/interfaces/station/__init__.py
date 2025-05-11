from .create import CreateStationInterface, CreateFavoriteInterface
from .delete import DeleteStationInterface, DeleteFavoriteInterface
from .read import GetStationInterface, GetStationsUrlsInterface, GetFavoriteInterface
from .update import UpdateStationInterface


__all__ = [
    "CreateStationInterface",
    "DeleteStationInterface",
    "GetStationInterface",
    "GetStationsUrlsInterface",
    "UpdateStationInterface",

    "CreateFavoriteInterface",
    "DeleteFavoriteInterface",
    "GetFavoriteInterface",
]
