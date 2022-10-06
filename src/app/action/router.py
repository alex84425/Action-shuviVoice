"""
This module contains some mandatory endpoints

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from vcosmosapiclient.custom_logging import log_wrapper
from vcosmosapiclient.depends import ApiDepends, FakeDepends
from vcosmosapiclient.utils import validator

from app.action import executor, models
from app.config import Settings, get_fake_settings, get_settings

router = APIRouter()


@router.get("/info")
async def info(config: Settings = Depends(get_settings)):
    return {"type": config.PROJECT_NAME, "typeVer": config.VERSION, "sourceVer": config.SOURCE_VERSION}


@router.get("/health")
async def health(config: Settings = Depends(get_settings)):
    url = f"http://127.0.0.1:{config.UUT_PROXY_DEFAULT_PORT}"

    async with httpx.AsyncClient() as client:
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
            detail=f"There's a problem accessing UUT proxy, status code: {response.status_code}",
        )

    return {"status": "ok"}


@router.post("/dryrun")
@validator.post
async def post_to_action_dryrun(act: models.MyActionPostModel, api: FakeDepends = Depends(), config: Settings = Depends(get_fake_settings)):
    # this endpoint may deprecated
    return await post_to_action(act, api, config)  # type: ignore


@router.post("/act")
@validator.post
async def post_to_action(act: models.MyActionPostModel, api: ApiDepends = Depends(), config: Settings = Depends(get_settings)):
    return await executor.execute_action(act)


@router.post("/onabort")
@log_wrapper
async def onabort(act: models.MyActionPostModel):
    try:
        return await executor.onabort(act)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot Abort, because of an error {exc}",
        ) from exc
