from pydantic import BaseModel


class AddFavorite(BaseModel):
    station_id: int
