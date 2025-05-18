from aiohttp import ClientSession


class NoService:

    def __init__(self) -> None:
        self.url = "https://naas.isalman.dev/no"

    async def get_reason(self, default_reason: str) -> str:
        reason = default_reason
        try:
            async with ClientSession() as session:
                async with session.get(self.url) as response:
                    if response.status == 200:
                        data = await response.json()
                        reason = data.get("reason")

        except Exception:
            pass
        return reason

    async def __call__(self, default_reason: str) -> str:
        return await self.get_reason(default_reason)
