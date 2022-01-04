# -*- coding: utf-8 -*-
from pathlib import Path

from app.action import router as action
from app.config import get_settings
from app.custom_logging import setup_logging
from app.health import router as health
from fastapi import FastAPI

config_path = Path(__file__).with_name("logging_config.json")
setup_logging(config_path)

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description=get_settings().PROJECT_NAME,
    version=get_settings().VERSION,
    root_path=get_settings().PREFIX,
)


app.include_router(health.router, tags=["health"])
app.include_router(action.router, tags=["action"], prefix="/action")
