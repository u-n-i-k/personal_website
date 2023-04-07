import datetime
import functools
import io
import logging
import random
import re
import string
import threading
import time
from contextlib import redirect_stderr, redirect_stdout
from enum import Enum
from typing import Any, Callable

import pycron
from fastapi import Request, Response
from fastapi.routing import APIRoute

log = logging.getLogger()


class Singleton(type):
    instance: Any = None
    _lock = threading.Lock()

    def __call__(cls, *args: list, **kwargs: dict) -> Any:
        with cls._lock:
            if cls.instance is not None:
                raise RuntimeError("{} instance already exists".format(cls))
            cls.instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls.instance


def rand_name(length: int = 16) -> str:
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(length))


def string_to_camel_case(s: str) -> str:
    return re.sub(
        "[^a-zA-Z]", "", "".join([part.title() for part in re.split("-|_", s)])
    )


def check_and_format_date_for_work_exp(date: datetime.date) -> str:
    if not isinstance(date, datetime.date):
        raise TypeError(f"start_dt expected to be datetime.date, {type(date)} found")
    return date.strftime("%Y/%m")


def parse_and_return_output(func: Callable) -> Callable:
    @functools.wraps(func)
    def _wrapper(*args: Any, **kwargs: Any) -> str:
        with io.StringIO() as buf, redirect_stdout(buf), redirect_stderr(buf):
            func(*args, **kwargs)
            res = buf.getvalue()
        return res

    return _wrapper


class ArgEnum(Enum):
    def __str__(self) -> str:
        return str(self.value)


class PyCronJob:
    def __init__(self, crontab: str, timeout: int | None = None):
        self.crontab = crontab
        self.timeout = timeout
        self.start_time = time.time()

    def do_job(self) -> None:
        raise NotImplementedError

    def check_for_timeout(self) -> None:
        if self.timeout is None:
            return
        if time.time() - self.start_time > self.timeout:
            raise TimeoutError("killed by timeout")

    def run(self) -> None:
        while True:
            self.check_for_timeout()
            if pycron.is_now(self.crontab):
                self.do_job()
            time.sleep(0.1)


def get_all_subclasses(cls: type) -> set:
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in get_all_subclasses(c)]
    )


class TimedRoute(APIRoute):
    def get_route_handler(self) -> callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            start_ts = time.time()
            response: Response = await original_route_handler(request)
            duration = time.time() - start_ts
            response.headers["X-Response-Time"] = str(duration)
            log.info("%s took %.3f ms", request.url.path, duration * 1000)
            return response

        return custom_route_handler
