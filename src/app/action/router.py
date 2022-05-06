# -*- coding: utf-8 -*-
"""
This module contains some mandatory endpoints

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""


import logging

from app.action import models
from app.action.executor import monitor_task_error
from app.config import Settings, get_fake_settings, get_settings
from fastapi import APIRouter, Depends, HTTPException, status
from vcosmosapiclient.api import MonitorFileResponse
from vcosmosapiclient.depends import ApiDepends, FakeDepends
from vcosmosapiclient.utils import validator

router = APIRouter()


@router.get("/info")
async def info(config: Settings = Depends(get_settings)):
    return {"type": config.PROJECT_NAME, "typeVer": config.VERSION, "sourceVer": config.SOURCE_VERSION}


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/monitor/task")
async def router_action_task_monitor(task: models.ErrorMonitorModel):
    result = await monitor_task_error(task.workingDirectory)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No error found.",
        )
    else:
        return {"ErrorMsg": result}


@router.post("/dryrun")
@validator.post
async def post_to_action_dryrun(act: models.MyActionPostModel, api: FakeDepends = Depends(), config: Settings = Depends(get_fake_settings)):
    body = MonitorFileResponse(
        task_folder=act.context.workingDirectory,
        monitor_file="LOGS/ResultDetails.json",
        result_file="LOGS/ResultDetails.json",
        status_file="LOGS/status.json",
    ).dict()

    logging.info("this is template /action/dryrun")

    api.bios.fake_return["get_bios_on_remote"] = {
        "Manufacturing Programming Mode": "Lock",
        "Serial Number": "0123456789",
        "Universally Unique Identifier (UUID)": "11111111112222222222333333333344",
    }

    bios_value = await api.bios.get_bios_on_remote(act)
    logging.info(bios_value)
    return body


@router.post("/act")
@validator.post
async def post_to_action(act: models.MyActionPostModel, api: ApiDepends = Depends(), config: Settings = Depends(get_settings)):
    if act.actionData.data.MyTestData is not None:
        # return direct pass for this template
        raise validator.DirectStatusPass("test passed")
    else:
        # never go there for this template
        body = MonitorFileResponse(
            task_folder=act.context.workingDirectory,
            monitor_file="LOGS/ResultDetails.json",
            result_file="LOGS/ResultDetails.json",
            status_file="LOGS/status.json",
        ).dict()
        return body
