import logging

from fastapi import FastAPI

import uvicorn

from api import FastAPIApp

from config import Config, get_config

from container import setup_container


def get_app() -> FastAPI:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s  %(process)-7s %(module)-20s %(message)s',
    )

    config: Config = get_config()
    app = FastAPIApp(config.api).app

    setup_container(app, config)
    return app


if "__main__" == __name__:
    uvicorn.run(get_app(), host="0.0.0.0", port=8000, reload=True, lifespan="on")
