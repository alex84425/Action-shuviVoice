import httpx
import vcosmosapiclient
from fastapi import APIRouter, HTTPException, status

from app.config import Settings, get_settings, is_resource_exists

router = APIRouter()
settings: Settings = get_settings()


@router.get("/")
async def root():
    return {
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "history": settings.HISTORY,
        "commit id": settings.SOURCE_VERSION,
        "lib version": vcosmosapiclient.VERSION,
        "lib history": vcosmosapiclient.HISTORY,
    }


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}


@router.get("/action/info")
async def info():
    return {"type": settings.PROJECT_NAME, "typeVer": settings.VERSION, "sourceVer": settings.SOURCE_VERSION}


@router.get("/action/health")
async def health():
    url = "http://127.0.0.1:8888"

    async with httpx.AsyncClient(proxies={}) as client:
        try:
            response = await client.get(
                url,
                timeout=60,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"fail to access UUT Proxy, status : {exc}",
            ) from exc

    if response.status_code != status.HTTP_404_NOT_FOUND:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Unexpected response from UUT proxy, status code: {response.status_code}",
        )

    if not await is_resource_exists(settings.RESOURCE_FILE_LATEST) and not await is_resource_exists(settings.RESOURCE_FILE_BACKUP):
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Resource file not ready",
        )

    return {"status": "ok"}
