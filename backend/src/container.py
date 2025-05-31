from dishka import make_async_container
from dishka.integrations.arq import setup_dishka as setup_arq_dishka
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from api.service import oauth2_scheme

from config import Config

from providers import ApiProvider, AppProvider, DBProvider, ServiceProvider, TaskProvider

from workers import TaskManager


def setup_container(app: FastAPI | TaskManager, config: Config) -> None:
    providers = [ApiProvider(), AppProvider(), DBProvider(), ServiceProvider(), TaskProvider()]

    container = make_async_container(
        *providers,
        context={
            Config: config,
            OAuth2PasswordBearer: oauth2_scheme if isinstance(app, FastAPI) else None,
        },
    )

    if isinstance(app, FastAPI):
        setup_fastapi_dishka(container, app)

    elif isinstance(app, TaskManager):
        app.dishka_container = container
        setup_arq_dishka(container, worker_settings=app.arq_context)

    else:
        raise ValueError(
            f"create container can only be used for 'FastAPI' or 'TaskManager'. Cannot be used for '{type(app)}'"
        )
