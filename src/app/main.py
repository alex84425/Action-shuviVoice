# -*- coding: utf-8 -*-
import logging
from pathlib import Path

from app.action import router as action
from app.config import get_settings
from app.custom_logging import CustomizeLogger
from app.health import router as health
from fastapi import FastAPI

logger = logging.getLogger(__name__)
config_path = Path(__file__).with_name("logging_config.json")
settings = get_settings()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_NAME,
    version=settings.VERSION,
    # docs_url="/docs",
    # openapi_url="/openapi.json",
    root_path=settings.PREFIX,
)


app.logger = CustomizeLogger.make_logger(config_path)
app.include_router(health.router, tags=["health"])
app.include_router(action.router, prefix="/action", tags=["action"])
