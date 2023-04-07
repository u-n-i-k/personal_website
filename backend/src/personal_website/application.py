import logging

import gunicorn.app.base
from fastapi import APIRouter, FastAPI
from gunicorn.glogging import Logger
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from personal_website import api
from personal_website.core.config import LOGGING_CONFIG, Config, configure_logging
from personal_website.db.dbhelper import DBHelper

log = logging.getLogger()


class CustomFastAPIApp(FastAPI):
    def __init__(
        self,
        router: APIRouter,
    ) -> None:
        fastapi_config = Config.instance.fastapi
        db_conn_config = Config.instance.db_conn
        self.dbhelper = DBHelper(
            sqlalchemy_async_database_uri=db_conn_config.sqlalchemy_async_database_uri,
            dbschema=db_conn_config.dbschema,
            pool_timeout=5,
            pool_size=3,
            max_overflow=6,
            pool_recycle=3600,
            pool_pre_ping=True,
            echo_pool="debug",
            echo=True,
        )
        middlewares = []
        if fastapi_config.backend_cors_origins:
            middlewares.append(
                Middleware(
                    CORSMiddleware,
                    allow_origins=[
                        str(origin) for origin in fastapi_config.backend_cors_origins
                    ],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"],
                )
            )
        super().__init__(middleware=middlewares)
        self.include_router(api.router)


class App(gunicorn.app.base.BaseApplication):
    def __init__(self, config: Config) -> None:
        self.fastapi_app = CustomFastAPIApp(router=api.router)
        super().__init__()
        configure_logging()
        log.info(f"Running gunicorn with params:\n{self.cfg}")

    def load_config(self) -> None:
        # we can't iterate on Config.instance.gunicorn
        # because internal fields won't be excluded this way
        for key, value in Config.instance.gunicorn.dict().items():
            if key in self.cfg.settings and value is not None:
                self.cfg.set(key, value)

        self.cfg.set("access_log_format", "%(levelname)s:%(message)s")
        self.cfg.set("accesslog", "-")
        self.cfg.set("logconfig_dict", LOGGING_CONFIG)

    def load(self) -> CustomFastAPIApp:
        return self.fastapi_app
