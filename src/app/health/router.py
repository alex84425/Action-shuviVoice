import vcosmosapiclient
from app.config import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
async def root(config: Settings = Depends(get_settings)):
    return {
        "service": config.PROJECT_NAME,
        "version": config.VERSION,
        "history": config.HISTORY,
        "commit id": config.SOURCE_VERSION,
        "lib version": vcosmosapiclient.VERSION,
        "lib history": vcosmosapiclient.HISTORY,
    }


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}
