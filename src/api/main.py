from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import APIConfig

from . import auth
from . import station
from .exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    yield
    await app.state.dishka_container.close()


class FastAPIApp:

    def __init__(self, config: APIConfig):
        self.config: APIConfig = config

        self._app: FastAPI = FastAPI(
            title=self.config.title,
            version=self.config.version,
            debug=self.config.debug,
            lifespan=lifespan,
        )

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.allow_origins,
            allow_credentials=self.config.allow_credentials,
            allow_methods=self.config.allow_methods,
            allow_headers=self.config.allow_headers,
        )

        self.app.mount("/static", StaticFiles(directory="./static"), name="static")
        self.register_routers()

    def register_routers(self) -> None:
        register_exception_handlers(self._app)

        self._app.include_router(auth.router)
        self._app.include_router(station.router)

    @property
    def app(self) -> FastAPI:
        return self._app
