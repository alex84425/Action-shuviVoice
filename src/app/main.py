# -*- coding: utf-8 -*-
from pathlib import Path

from app.action import router as action
from app.config import get_settings
from app.custom_logging import setup_logging
from app.health import router as health
from fastapi import FastAPI

config_path = Path(__file__).with_name("logging_config.json")
settings = get_settings()


setup_logging(config_path)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_NAME,
    version=settings.VERSION,
    root_path=settings.PREFIX,
)


app.include_router(health.router, tags=["health"])
app.include_router(action.router, tags=["action"], prefix="/action")
