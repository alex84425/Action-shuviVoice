"""
This module contains some mandatory endpoints

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""
import asyncio
import logging

from app.action import executor, models
from app.config import Settings, get_fake_settings, get_settings
from fastapi import APIRouter, Depends, HTTPException, status
from vcosmosapiclient.depends import ApiDepends, FakeDepends
from vcosmosapiclient.utils import validator

router = APIRouter()


@router.get("/info")
async def info(config: Settings = Depends(get_settings)):
    return {"type": config.PROJECT_NAME, "typeVer": config.VERSION, "sourceVer": config.SOURCE_VERSION}


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/dryrun")
@validator.post
async def post_to_action_dryrun(act: models.MyActionPostModel, api: FakeDepends = Depends(), config: Settings = Depends(get_fake_settings)):
    # this endpoint may deprecated
    return await post_to_action(act, api, config)


@router.post("/act")
@validator.post
async def post_to_action(act: models.MyActionPostModel, api: ApiDepends = Depends(), config: Settings = Depends(get_settings)):
    return await executor.execute_action(act)


@router.post("/onabort")
async def onabort(on_abort_data: dict):
    logging.debug(f"{on_abort_data=}")
    task_name = on_abort_data["task_name"]

    for task in asyncio.all_tasks():
        if task.get_name() == task_name and not task.done():
            try:
                task.cancel()
                break
            except asyncio.CancelledError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"task is cancelled {task_name=}",
                )
    return {"status": "ok"}
