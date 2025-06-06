from application import dto
from application import interfaces

from db import domain


class CreateStation:

    def __init__(self, gateway: interfaces.CreateStationInterface):
        self.gateway = gateway

    async def __call__(
            self,
            data: dto.Station | list[dto.Station],
    ) -> int | list[int]:
        if isinstance(data, list):
            domain_data_list = [
                domain.CreateStationModel(**item.dict())
                for item in data
            ]
            return await self.gateway.create_stations(domain_data_list)

        domain_data = domain.CreateStationModel(**data.dict())
        return await self.gateway.create_station(domain_data)


class CreateFavorite:

    def __init__(self, gateway: interfaces.CreateFavoriteInterface):
        self.gateway = gateway

    async def __call__(
            self,
            user_id: int,
            station_id: int,
    ) -> int:
        return await self.gateway.create_favorite(user_id, station_id)
