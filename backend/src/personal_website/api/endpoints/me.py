from typing import Annotated

import sqlalchemy as sa
from fastapi import APIRouter, Depends, Request, Response, status
from pydantic import SecretStr

from personal_website import schemas
from personal_website.core.grecaptcha import (
    check_grecaptcha_token,
    get_grecaptcha_secret_token,
)
from personal_website.core.utils import TimedRoute
from personal_website.db.orm.common import AboutMe, ContactRequest
from personal_website.db.session import (
    AsyncSession,
    get_ro_async_session,
    get_transactional_async_session,
)

router = APIRouter(route_class=TimedRoute)


@router.get("/about", response_model=schemas.me.AboutMeSchema)
async def about(
    session: Annotated[AsyncSession, Depends(get_ro_async_session)], lang: str = "ru"
) -> AboutMe:
    stmt = sa.select(AboutMe).where(AboutMe.lang == lang)
    res = (await session.scalars(stmt)).one()
    return res


@router.post("/contact")
async def contact(
    session: Annotated[AsyncSession, Depends(get_transactional_async_session)],
    request: Request,
    params: schemas.me.ContactMeParamsSchema,
    grecaptcha_secret_token: Annotated[SecretStr, Depends(get_grecaptcha_secret_token)],
    response: Response,
) -> dict:
    try:
        check_grecaptcha_token(
            params.recaptcha_token,
            grecaptcha_secret_token,
            request.headers.get("X-Forwarded-For"),
        )
        contact_request = ContactRequest(email=params.email, message=params.message)
        session.add(contact_request)

    except ValueError as err:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"result": "error", "details": str(err)}
    except RuntimeError as err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"result": "error", "details": str(err)}

    return {"result": "success"}
