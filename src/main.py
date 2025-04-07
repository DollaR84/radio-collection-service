import logging

import coloredlogs

from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka

from fastapi import FastAPI

import uvicorn

from api import FastAPIApp

from config import Config

from providers import DBProvider


def get_app() -> FastAPI:
    coloredlogs.install()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s  %(process)-7s %(module)-20s %(message)s',
    )

    config = Config()
    app = FastAPIApp().create(config)

    container = make_async_container(
        DBProvider(),
        context={Config: config},
    )

    setup_dishka(container, app)
    return app


if "__main__" == __name__:
    uvicorn.run(get_app(), host="0.0.0.0", port=8000, reload=True, lifespan="on")
