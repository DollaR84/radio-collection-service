from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from config import APIConfig

from . import auth
from .exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


class FastAPIApp:

    def __init__(self, config: APIConfig):
        self.config: APIConfig = config

        self._app: FastAPI = FastAPI(
            title="Radio Collection Service API",
            debug=self.config.debug,
            lifespan=lifespan,
        )

        self._app.include_router(auth.router)

        register_exception_handlers(self._app)

    @property
    def app(self) -> FastAPI:
        return self._app
