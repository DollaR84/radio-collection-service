from application import interfaces


class DeleteStation:

    def __init__(self, gateway: interfaces.DeleteStationInterface):
        self.gateway = gateway

    async def __call__(
            self,
            station_id: int,
    ) -> None:
        await self.gateway.delete_station(station_id)
