import json
import logging.config
import multiprocessing
from typing import Annotated, Any, ClassVar

from pydantic import (
    AnyHttpUrl,
    BaseModel,
    DirectoryPath,
    FilePath,
    IPvAnyAddress,
    PostgresDsn,
    SecretStr,
    conint,
    constr,
    root_validator,
    validator,
)
from pydantic.main import ModelMetaclass

from personal_website.core.utils import Singleton

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "pretty": {
            # "()": "logging.Formatter",
            "format": "%(asctime)s [%(process)d] %(levelname)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": """
                    asctime: %(asctime)s
                    created: %(created)f
                    filename: %(filename)s
                    funcName: %(funcName)s
                    levelname: %(levelname)s
                    levelno: %(levelno)s
                    lineno: %(lineno)d
                    message: %(message)s
                    module: %(module)s
                    msec: %(msecs)d
                    name: %(name)s
                    pathname: %(pathname)s
                    process: %(process)d
                    processName: %(processName)s
                    relativeCreated: %(relativeCreated)d
                    thread: %(thread)d
                    threadName: %(threadName)s
                    exc_info: %(exc_info)s
                """,
            "datefmt": "%Y-%m-%dT%H:%M:%S%z",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "formatter": "pretty",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "error_console": {
            "formatter": "pretty",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "json": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "gunicorn.error": {
            "level": "ERROR",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "gunicorn.error",
        },
        "gunicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": True,
            "qualname": "gunicorn.access",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
        "qualname": "personal_website",
    },
}


def configure_logging():
    logging.config.dictConfig(LOGGING_CONFIG)


class ConfigSingleton(ModelMetaclass, Singleton):
    pass


class ModelWithRestrictedFields(BaseModel):
    restricted_fields: ClassVar[list[str]] = []

    @root_validator(pre=True)
    def check_restricted_fields_not_specified(cls, values: dict) -> dict:
        for field in cls.restricted_fields:
            if field in values:
                raise ValueError(f"{field} should not be included")
        return values


class DBConnectionConfig(BaseModel):
    server: str
    port: conint(ge=1, le=65535) = 5432  # type: ignore
    user: str
    password_secret: FilePath
    password: SecretStr | None = None
    dbname: str
    dbschema: str

    @root_validator(pre=True)
    def check_password_is_not_specified(cls, values: dict) -> dict:
        if "password" in values:
            raise ValueError("password should not be included")
        return values

    @validator("password", always=True)
    def read_password_from_secret(
        cls, password: SecretStr | None, values: dict
    ) -> SecretStr:
        if "password_secret" not in values:
            raise ValueError("missing file for password_secret")
        with open(values["password_secret"], "r") as f:
            password = SecretStr(f.read().strip())
        return password

    @property
    def sqlalchemy_async_database_uri(self) -> str:
        return PostgresDsn.build(  # type: ignore
            scheme="postgresql+asyncpg",
            user=self.user,
            password=self.password.get_secret_value(),  # type: ignore
            host=self.server,
            path=f"/{self.dbname}",
        )


class FastAPIConfig(BaseModel):
    backend_cors_origins: list[AnyHttpUrl] = []
    grecaptcha_secret_token_secret: FilePath
    grecaptcha_secret_token: SecretStr | None = None

    @root_validator(pre=True)
    def check_password_is_not_specified(cls, values: dict) -> dict:
        if "grecaptcha_secret_token" in values:
            raise ValueError("grecaptcha_secret_token should not be included")
        return values

    @validator("grecaptcha_secret_token", always=True)
    def read_grecaptcha_secret_token_from_secret(
        cls, password: SecretStr | None, values: dict
    ) -> SecretStr:
        if "grecaptcha_secret_token_secret" not in values:
            raise ValueError("missing file for grecaptcha_secret_token_secret")
        with open(values["grecaptcha_secret_token_secret"], "r") as f:
            grecaptcha_secret_token = SecretStr(f.read().strip())
        return grecaptcha_secret_token


class GunicornConfig(ModelWithRestrictedFields):
    # https://docs.gunicorn.org/en/stable/settings.html
    restricted_fields: ClassVar[list[str]] = ["bind", "logger_class"]

    timeout: int = 10
    worker_class: str = "uvicorn.workers.UvicornWorker"
    workers: int = multiprocessing.cpu_count() * 2 + 1
    # TODO: validation for hostnames
    host: IPvAnyAddress | Annotated[str, constr(regex="^[a-zA-Z\d\-\.]+$")]
    port: Annotated[int, conint(ge=1, le=65535)] = 8080
    bind: str | None = None

    @validator("bind", always=True)
    def construct_bind_from_ip_and_port(cls, bind: str | None, values: dict) -> str:
        return f"{values['host']}:{values['port']}"

    class Config:
        fields = {
            "host": {"exclude": True},
            "port": {"exclude": True},
        }


class TelegramSenderConfig(ModelWithRestrictedFields):
    restricted_fields: ClassVar[list[str]] = ["bot_token"]
    bot_token_secret: FilePath
    bot_token: SecretStr | None = None
    notification_chat_id: int

    @validator("bot_token", always=True)
    def read_bot_token_secret(
        cls, bot_token: SecretStr | None, values: dict
    ) -> SecretStr:
        if "bot_token_secret" not in values:
            raise ValueError(f"missing filename of bot_token secret: {values}")
        with open(values["bot_token_secret"], "r") as f:
            bot_token = SecretStr(f.read().strip())
        return bot_token


class Config(BaseModel, metaclass=ConfigSingleton):
    db_conn: DBConnectionConfig
    fastapi: FastAPIConfig
    gunicorn: GunicornConfig
    tg_sender: TelegramSenderConfig
    secrets_dir: DirectoryPath

    @root_validator(pre=True)
    def add_prefix_path_for_secrets(cls, values: dict) -> dict:
        def _add_prefix_path_for_secrets(values: dict, secrets_dir: str) -> None:
            for key in values:
                is_dict = isinstance(values[key], dict)
                if is_dict:
                    _add_prefix_path_for_secrets(values[key], secrets_dir)
                if "secret" in key.split("_"):
                    values[key] = "{}/{}".format(secrets_dir.rstrip("/"), values[key])

        _add_prefix_path_for_secrets(values, values["secrets_dir"])

        return values
