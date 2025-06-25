from config import AdminConfig, Config

from fastapi import FastAPI

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.staticfiles import StaticFiles

from sqladmin import Admin

from sqlalchemy.ext.asyncio import AsyncEngine

from .auth import AdminAuth
from .middlewares import DishkaAdminMiddleware, InjectStaticMiddleware
from .models import (
    AccessPermissionAdmin,
    FavoriteAdmin,
    StationAdmin,
    UserAdmin,
)


class AdminApp:

    @classmethod
    async def create(cls, app: FastAPI) -> None:
        config = await app.state.container.get(Config)
        engine = await app.state.container.get(AsyncEngine)

        admin_auth = AdminAuth(config)
        admin_app = cls(config.admin, app, engine, admin_auth)
        app.state.admin_app = admin_app

        app.mount("/", admin_app.app)

    def __init__(self, config: AdminConfig, app: FastAPI, engine: AsyncEngine, admin_auth: AdminAuth):
        self.config = config

        css_urls = [
            "/static/css/base.css",
            "/static/css/tags-manager.css",
        ]
        js_urls = ["/static/js/tags-manager.js"]

        self._app = Starlette(
            routes=[],
            middleware=[
                Middleware(DishkaAdminMiddleware, container=app.state.container),
            ],
        )

        self._app.add_middleware(InjectStaticMiddleware, js_urls=js_urls, css_urls=css_urls)
        self._app.mount("/admin/static", StaticFiles(directory="/app/static"), name="admin_static")

        admin = Admin(
            self._app,
            engine,
            authentication_backend=admin_auth,
            title=self.config.title,
            base_url=self.config.base_url,
            templates_dir=self.config.templates_dir,
        )

        self.register(admin)

    @property
    def app(self) -> Starlette:
        if self._app is None:
            raise RuntimeError("admin application is not initialized")

        return self._app

    def register(self, admin: Admin) -> None:
        views = (
            UserAdmin,
            AccessPermissionAdmin,
            StationAdmin,
            FavoriteAdmin,
        )

        for view in views:
            admin.add_view(view)
