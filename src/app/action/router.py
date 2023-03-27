"""
This module contains some mandatory endpoints

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""
import datetime

from fastapi import APIRouter, HTTPException, status
from vcosmosapiclient.api import MonitorFileResponse
from vcosmosapiclient.custom_logging import log_wrapper
from vcosmosapiclient.utils import validator

from app.action import executor, models
from app.config import Settings, get_settings

router = APIRouter()
settings: Settings = get_settings()
TEN_MINUTES_IN_MICROSECONDS = int(datetime.timedelta(minutes=10).total_seconds() * 1000)  # for axios


@router.post("/act")
@validator.post
async def post_to_action(act: models.MyActionPostModel):
    # raise validator.DirectStatusPass() for direct pass
    # raise raise RuntimeError() for direct fail

    # Basic router hook for action
    response = MonitorFileResponse(
        task_folder=act.context.workingDirectory,
        monitor_file="LOGS/status.txt",
        result_file="LOGS/ResultDetails.json",
        status_file="LOGS/status.txt",
    ).dict()

    # example of onStart and onStop callback
    headers = {"Content-type": "application/json"}
    response["monitorOnStart"] = [
        {
            "executeType": "targetCommand",
            "environmentVariables": {},
            "workingDirectory": str(act.context.workingDirectory),
            "waitFinished": True,
            "command": ["powershell.exe", "echo", "start", ">", "_start.log"],
        },
        {
            "executeType": "request",
            "url": f"http://{settings.HOSTNAME_AND_PORT}/action/onstart",
            "method": "POST",
            "headers": headers,
            "data": {"example_extra_data": "for_onstart"},
            "timeout": TEN_MINUTES_IN_MICROSECONDS,
        },
    ]
    response["monitorOnStop"] = [
        {
            "executeType": "targetCommand",
            "environmentVariables": {},
            "workingDirectory": str(act.context.workingDirectory),
            "waitFinished": True,
            "command": ["powershell.exe", "echo", "stop", ">", "_stop.log"],
        },
        {
            "executeType": "request",
            "url": f"http://{settings.HOSTNAME_AND_PORT}/action/onstop",
            "method": "POST",
            "headers": headers,
            "data": {"example_extra_data": "for_onstop"},
            "timeout": TEN_MINUTES_IN_MICROSECONDS,
        },
    ]

    # example of onAbort callback
    response["onAbort"] = [
        {
            "executeType": "request",
            "url": f"http://{settings.HOSTNAME_AND_PORT}/action/onabort",
            "method": "POST",
            "headers": headers,
            "data": {"example_extra_data": "for_onabort"},
            "timeout": TEN_MINUTES_IN_MICROSECONDS,
        },
    ]

    return response


@router.post("/onstart")
@log_wrapper
async def onstart(payload: models.MyActionCallbackModel):
    try:
        return await executor.onstart(payload.act)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot Start, because of an error {exc}, try again.",
        ) from exc


@router.post("/onstop")
@log_wrapper
async def onstop(payload: models.MyActionCallbackModel):
    try:
        return await executor.onstop(payload.act)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot Stop, because of an error {exc}, try again.",
        ) from exc


@router.post("/onabort")
@log_wrapper
async def onabort(payload: models.MyActionCallbackModel):
    try:
        return await executor.onabort(payload.act)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Cannot Abort, because of an error {exc}, no more try",
        ) from exc
