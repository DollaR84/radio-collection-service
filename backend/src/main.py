import logging

from fastapi import FastAPI

from api import FastAPIApp

from config import Config, get_config

from container import setup_container


def get_app() -> FastAPI:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s  %(process)-7s %(module)-20s %(message)s',
    )

    config: Config = get_config()
    _app = FastAPIApp(config.api).app

    setup_container(_app, config)
    return _app


app = get_app()
