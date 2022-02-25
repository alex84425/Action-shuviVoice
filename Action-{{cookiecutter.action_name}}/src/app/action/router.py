# -*- coding: utf-8 -*-
import asyncio
import logging

from app.action import models
from app.config import FakeSettings, Settings, get_fake_settings, get_settings
from fastapi import APIRouter, Depends
from vcosmosapiclient.api import MonitorFileResponse
from vcosmosapiclient.depends import ApiDepends, FakeDepends
from vcosmosapiclient.utils import validator
from executor import main_task_handler, monitor_task_error

router = APIRouter()


@router.get("/info")
async def info(config: Settings = Depends(get_settings)):
    """
    Required endpoint
    https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract
    """  # noqa
    return {"type": config.PROJECT_NAME, "typeVer": config.VERSION}


@router.get("/health")
async def health():
    """
    Required endpoint
    https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract
    """  # noqa
    return {"status": "ok"}


@router.post("/monitor/task")
async def router_action_task_monitor(task: models.ErrorMonitorModel):
    result = await monitor_task_error(task.workingDirectory)
    if not result:
        return {}
    else:
        return {
            "ErrorMsg": result
        }


@router.post("/dryrun")
@validator.post
async def post_to_action_dryrun(
    act: models.MyActionPostModel, api: FakeDepends = Depends(), config: FakeSettings = Depends(get_fake_settings)
):
    """
    Required endpoint
    https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

    Response schema:
    https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
    """  # noqa

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

    bios_value = api.bios.get_bios_on_remote(act)
    logging.info(bios_value)
    return body


@router.post("/act")
@validator.post
async def post_to_action(
    act: models.MyActionPostModel, api: ApiDepends = Depends(), config: Settings = Depends(get_settings)
):
    """
    Required endpoint
    https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

    Response schema:
    https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
    """  # noqa
    task = asyncio.current_task()
    task.set_name(act.sub_task_id()[-8:])

    body = MonitorFileResponse(
        task_folder=act.context.workingDirectory,
        monitor_file="LOGS/ResultDetails.json",
        result_file="LOGS/ResultDetails.json",
        status_file="LOGS/status.json",
    ).dict()

    monitor_data = models.ErrorMonitorModel(workingDirectory=act.context.workingDirectory)
    project_name = get_settings().PROJECT_NAME.lower()

    errorOccurRequestData = {
        "url": f"http://{project_name}:8080/action/monitor/task",
        "method": "POST",
        "headers": {
            "Content-type": "application/json"
        },
        "data": monitor_data.json(),
        "timeout": 3600,
    }

    body.update({"errorOccurType": "request",
                 "errorOccurRequestData": errorOccurRequestData})

    logging.info("this is template /action/act")

    result = await main_task_handler(act, api)
    logging.info(result)
    return body
