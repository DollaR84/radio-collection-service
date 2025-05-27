from dishka import make_async_container
from dishka.integrations.arq import setup_dishka as setup_arq_dishka
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from api.service import oauth2_scheme

from config import Config

from providers import ApiProvider, AppProvider, DBProvider, ServiceProvider, TaskProvider

from workers import ArqContext


def setup_container(app_ctx: FastAPI | ArqContext, config: Config) -> None:
    providers = [ApiProvider(), AppProvider(), DBProvider(), ServiceProvider(), TaskProvider()]

    container = make_async_container(
        *providers,
        context={
            Config: config,
            OAuth2PasswordBearer: oauth2_scheme if isinstance(app_ctx, FastAPI) else None,
        },
    )

    if isinstance(app_ctx, FastAPI):
        setup_fastapi_dishka(container, app_ctx)

    elif isinstance(app_ctx, ArqContext):
        app_ctx.dishka_container = container
        setup_arq_dishka(container, worker_settings=app_ctx)
    else:
        raise ValueError(
            f"create container can only be used for 'FastAPI' or 'ArqContext'. Cannot be used for '{type(app_ctx)}'"
        )
