import logging
from datetime import datetime

import vcosmosapiclient
from fastapi import FastAPI
from vcosmosapiclient.custom_logging import setup_logging

from app.action import router as action
from app.config import get_settings
from app.debug import router as debug
from app.health import router as health

config = get_settings()
setup_logging(str(config.LOG_FOLDER / "debug.log"))
logging.info(config)


DESCRIPTION = f"""
    service: {config.PROJECT_NAME}
    version: {config.VERSION}
    history: {list(config.HISTORY.values())[0]}
    commit id: {config.SOURCE_VERSION}
    lib version: {vcosmosapiclient.VERSION}
    lib history: {list(vcosmosapiclient.HISTORY.values())[0]}
    deployed time: {datetime.now(timezone(timedelta(hours=+8))).ctime()}
    """


app = FastAPI(
    title=config.PROJECT_NAME,
    description=DESCRIPTION,
    version=config.VERSION,
    root_path=config.PATH_PREFIX,
)

app.include_router(health.router, tags=["health"])
app.include_router(action.router, tags=["action"], prefix="/action")
app.include_router(debug.router, tags=["debug"])
