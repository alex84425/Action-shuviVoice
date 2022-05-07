import vcosmosapiclient
from app.action import router as action
from app.config import get_settings
from app.debug import router as debug
from app.health import router as health
from fastapi import FastAPI
from vcosmosapiclient.custom_logging import setup_logging

setup_logging()

config = get_settings()
description = f"""
    service: {config.PROJECT_NAME}
    version: {config.VERSION}
    history: {list(config.HISTORY.values())[0]}
    commit id: {config.SOURCE_VERSION}
    lib version: {vcosmosapiclient.VERSION}
    lib history: {list(vcosmosapiclient.HISTORY.values())[0]}
"""

app = FastAPI(
    title=config.PROJECT_NAME,
    description=description,
    version=config.VERSION,
    root_path=config.PREFIX,
)

app.include_router(health.router, tags=["health"])
app.include_router(action.router, tags=["action"], prefix="/action")
app.include_router(debug.router, tags=["debug"])
