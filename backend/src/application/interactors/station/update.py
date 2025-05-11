from application import dto
from application import interfaces
from db import domain


class BaseUpdateStation:

    def __init__(self, gateway: interfaces.UpdateStationInterface):
        self.gateway = gateway


class UpdateStationStatus(BaseUpdateStation):

    async def __call__(self, update_data: dto.UpdateStationStatus) -> int:
        domain_data = domain.UpdateStationStatusModel(**update_data.dict())
        return await self.gateway.update_station_status(domain_data)


class UpdateStationsStatus(BaseUpdateStation):

    async def __call__(self, update_data: list[dto.UpdateStationStatus]) -> list[int]:
        domain_data = [domain.UpdateStationStatusModel(**data.dict()) for data in update_data]
        return await self.gateway.update_stations_status(domain_data)
