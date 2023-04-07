import logging
import time
from typing import Annotated

import sqlalchemy as sa
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.routing import APIRoute

from personal_website import schemas
from personal_website.core.utils import TimedRoute
from personal_website.db.session import (
    AsyncSession,
    get_ro_async_session,
    get_transactional_async_session,
)

router = APIRouter(route_class=TimedRoute)


@router.get("/ping", response_model=schemas.utils.TestMsg, status_code=200)
async def test() -> dict:
    return {"result": "success"}


@router.get("/ping-db", response_model=schemas.utils.TestMsg, status_code=200)
async def ping_db(
    session: Annotated[AsyncSession, Depends(get_transactional_async_session)]
) -> dict:
    try:
        res = await session.execute(
            sa.text("select test from (values('success')) t(test);")
        )
    except Exception as err:
        raise HTTPException(status_code=500, detail={"result": "error"})
    return {"result": str(res.all()[0][0])}
