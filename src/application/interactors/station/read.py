from application import interfaces


class GetStationUrls:

    def __init__(self, gateway: interfaces.GetStationInterface):
        self.gateway = gateway

    async def __call__(self) -> list[str]:
        return await self.gateway.get_stations_urls()
