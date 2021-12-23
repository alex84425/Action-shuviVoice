# -*- coding: utf-8 -*-
from fastapi import APIRouter

from app.api.api_v1.endpoints import action, ping

# FIXME temp solution
# api_router = APIRouter()
# api_router.include_router(ping.router, tags=["ping"])
# api_router.include_router(action.router, prefix="/info", tags=["info"])
