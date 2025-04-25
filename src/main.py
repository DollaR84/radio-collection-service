import logging

import coloredlogs

from fastapi import FastAPI

import uvicorn

from api import FastAPIApp

from config import Config

from container import setup_container


def get_app() -> FastAPI:
    coloredlogs.install()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s  %(process)-7s %(module)-20s %(message)s',
    )

    config = Config()
    app = FastAPIApp(config.api).app

    setup_container(app, config)
    return app


if "__main__" == __name__:
    uvicorn.run(get_app(), host="0.0.0.0", port=8000, reload=True, lifespan="on")
