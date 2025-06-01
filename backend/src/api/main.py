from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from dishka.integrations.fastapi import DishkaRoute

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.utils import get_openapi

from config import APIConfig

from . import auth
from . import favorite
from . import station
from . import tasks

from . import service
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
            description=self.config.description,
            debug=self.config.debug,
            lifespan=lifespan,
            swagger_ui_oauth2_redirect_url=self.swagger_ui_oauth2_redirect_url,
            swagger_ui_parameters=self.swagger_ui_parameters,
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

        self.configure_openapi()

    @property
    def swagger_ui_parameters(self) -> dict[str, Any]:
        return {
            "syntaxHighlight.theme": "obsidian",
            "displayRequestDuration": True,
            "tryItOutEnabled": True,
            "persistAuthorization": True,
        }

    @property
    def swagger_ui_oauth2_redirect_url(self) -> str:
        return "/oauth2-redirect"

    def configure_openapi(self) -> None:
        def custom_openapi() -> dict[str, Any]:
            if self._app.openapi_schema:
                return self._app.openapi_schema

            openapi_schema = get_openapi(
                title=self.config.title,
                version=self.config.version,
                description=self.config.description,
                routes=self._app.routes,
            )

            components = openapi_schema.setdefault("components", {})
            security_schemes = components.setdefault("securitySchemes", {})
            security_schemes.setdefault("Bearer", {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Enter: **Bearer&lt;space&gt;Token**",
            })
            openapi_schema["security"] = [{"Bearer": []}]

            self._app.openapi_schema = openapi_schema
            return self._app.openapi_schema

        self._app.openapi = custom_openapi  # type: ignore[method-assign]

    def register_routers(self) -> None:
        register_exception_handlers(self._app)
        main_router = APIRouter(prefix="/api", route_class=DishkaRoute)

        main_router.include_router(auth.router, tags=["auth", "user"])
        main_router.include_router(service.router, tags=["service"])
        main_router.include_router(station.router, tags=["station"])
        main_router.include_router(favorite.router, tags=["favorite"])
        main_router.include_router(tasks.router, tags=["task"])

        self._app.include_router(main_router)

    @property
    def app(self) -> FastAPI:
        return self._app
