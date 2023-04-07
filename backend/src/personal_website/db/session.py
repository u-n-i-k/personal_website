from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from personal_website.core.config import Config
from personal_website.db.dbhelper import DBHelper


async def get_ro_async_session(request: Request, strict: bool = True) -> AsyncGenerator:
    def make_ro(session: AsyncSession, strict: bool) -> AsyncSession:
        async def raise_session_is_ro_error(*args: Any, **kwargs: Any) -> Any:
            raise Exception("session is read only")

        async def do_nothing(*args: Any, **kwargs: Any) -> Any:
            pass

        if strict:
            session.flush = raise_session_is_ro_error  # type: ignore
        session.commit = do_nothing  # type: ignore

        return session

    dbhelper = request.app.dbhelper
    session = make_ro(dbhelper.create_async_session(), strict)
    yield session
    await session.close()


async def get_transactional_async_session(request: Request) -> AsyncGenerator:
    dbhelper = request.app.dbhelper
    session = dbhelper.create_async_session()
    session.begin()
    try:
        yield session
        await session.commit()
    except Exception as err:
        await session.rollback()
        raise err
    finally:
        await session.close()
