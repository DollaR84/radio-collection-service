from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import Config

from .exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


class FastAPIApp:

    def __init__(self, config: Config):
        self.config: Config = config

        self._app: FastAPI = FastAPI(
            title="Radio Collection Service API",
            debug=self.config.api.debug,
            lifespan=lifespan,
        )

        register_exception_handlers(self._app)

    @property
    def app(self) -> FastAPI:
        return self._app
