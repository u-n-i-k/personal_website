import logging
import time

from fastapi import APIRouter, Request, Response
from fastapi.routing import APIRoute

from personal_website.api import endpoints
from personal_website.core.utils import TimedRoute

log = logging.getLogger()


router = APIRouter(route_class=TimedRoute)
router.include_router(endpoints.utils.router, prefix="/utils", tags=["utils"])
router.include_router(endpoints.me.router, prefix="/me", tags=["me"])
router.include_router(endpoints.work.router, prefix="/work", tags=["work"])
