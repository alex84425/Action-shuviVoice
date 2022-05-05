from app.action import router as action
from app.config import get_settings
from app.health import router as health
from fastapi import FastAPI
from vcosmosapiclient.custom_logging import setup_logging
from vcosmosapiclient.middlewares import RequestContextLogMiddleware


setup_logging()

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description=get_settings().PROJECT_NAME,
    version=get_settings().VERSION,
    root_path=get_settings().PREFIX,
)
app.add_middleware(RequestContextLogMiddleware)

app.include_router(health.router, tags=["health"])
app.include_router(action.router, tags=["action"], prefix="/action")
