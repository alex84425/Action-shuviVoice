# -*- coding: utf-8 -*-
from fastapi import FastAPI

# from app.api.api_v1.api import api_router
from app.core.config import get_settings

settings = get_settings()

# app = FastAPI(
#     root_path="/",
#     title=settings.PROJECT_NAME,
#     openapi_url=f"{settings.API_V1_STR}/openapi.json",
# )

# app.include_router(api_router, prefix=settings.API_V1_STR)

# FIXME testing
from app.api.api_v1.endpoints import action, ping


app = FastAPI(title="SMR Cloud Service",
              description="This is implemented by parsing smr website.",
              version="1.0.0",
              servers=[
                  {"url": "/"},
                  {"url": settings.API_V1_STR}
              ],
              docs_url=f"{settings.API_V1_STR}/docs",
              openapi_url=f"{settings.API_V1_STR}/openapi.json")

app.include_router(ping.router, prefix=settings.API_V1_STR,)
app.include_router(action.router, prefix=settings.API_V1_STR, tags="action")
