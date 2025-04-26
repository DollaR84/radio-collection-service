from dishka import make_async_container
from dishka.integrations.arq import setup_dishka as setup_arq_dishka
from dishka.integrations.fastapi import setup_dishka as setup_fastapi_dishka

from fastapi import FastAPI

from config import Config

from providers import AppProvider, DBProvider, ServiceProvider, TaskProvider

from workers import ArqContext


def setup_container(context: FastAPI | ArqContext, config: Config) -> None:
    providers = [AppProvider(), DBProvider(), ServiceProvider(), TaskProvider()]

    container = make_async_container(
        *providers,
        context={Config: config},
    )

    if isinstance(context, FastAPI):
        setup_fastapi_dishka(container, context)
    elif isinstance(context, ArqContext):
        setup_arq_dishka(container, worker_settings=context)
    else:
        raise ValueError(
            f"create container can only be used for 'FastAPI' or 'ArqContext'. Cannot be used for '{type(context)}'"
        )
