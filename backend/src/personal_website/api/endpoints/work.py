import time
from collections import namedtuple
from typing import Annotated, Callable

import sqlalchemy as sa
from fastapi import APIRouter, Depends, Request, Response
from fastapi.routing import APIRoute
from sqlalchemy.orm import contains_eager

from personal_website import schemas
from personal_website.core.utils import TimedRoute
from personal_website.db.orm.common import localized_work_experiences
from personal_website.db.session import AsyncSession, get_ro_async_session

router = APIRouter(route_class=TimedRoute)

WorkHistory = namedtuple("WorkHistory", ["history"])


@router.get("/history", response_model=schemas.work.WorkHistorySchema, status_code=200)
async def history(
    session: Annotated[AsyncSession, Depends(get_ro_async_session)], lang: str = "ru"
) -> WorkHistory:
    WorkExp = localized_work_experiences[lang]
    stmt = sa.select(WorkExp).order_by(WorkExp.start_dt.desc())
    res = (await session.scalars(stmt)).all()
    return WorkHistory(history=res)
