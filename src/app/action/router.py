"""This module contains some mandatory endpoints.

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""
import datetime
import logging

from fastapi import APIRouter, HTTPException, status
from vcosmosapiclient.api_proxy import execute_ps1_on_remote, send_file_to_remote
from vcosmosapiclient.custom_logging import log_wrapper
from vcosmosapiclient.errors import UutConnectionError
from vcosmosapiclient.utils import validator

import static
from app.action import executor, models
from app.config import Settings, get_settings

router = APIRouter()
settings: Settings = get_settings()
HEADERS = {"Content-type": "application/json"}
TEN_MINUTES_IN_MICROSECONDS = int(datetime.timedelta(minutes=10).total_seconds() * 1000)  # for axios


@router.post("/act")
@validator.post
async def post_to_action(act: models.MyActionPostModel):
    # send action files
    await send_file_to_remote(act.target, static.file("monitorOnStart.cmd"), act.context.workingDirectory, override=True)
    await send_file_to_remote(act.target, static.file("monitorOnStart.ps1"), act.context.workingDirectory, override=True)
    await send_file_to_remote(act.target, static.file("monitorOnStop.ps1"), act.context.workingDirectory, override=True)
    await send_file_to_remote(act.target, static.file("onAbort.ps1"), act.context.workingDirectory, override=True)
    await send_file_to_remote(act.target, static.file("monitorTargetData.ps1"), act.context.workingDirectory, override=True)

    response = {
        "monitorType": "exist",
        "monitorTargetType": "request",
        "monitorTargetData": {
            "url": f"http://{settings.HOSTNAME_AND_PORT}/action/monitor/target",
            "method": "POST",
            "headers": {"Content-type": "application/json"},
            "timeout": TEN_MINUTES_IN_MICROSECONDS,
        },
        "monitorBehavior": "stop",
        "monitorIntervalInSecs": 10,
        "monitorTimeoutInSecs": int(datetime.timedelta(minutes=10).total_seconds()),
        "resultType": "file",
        "resultGetRequestData": str(act.context.workingDirectory / "LOGS/result.txt"),  # for result action (sherlock)
        "storeType": "file",
        "storeGetRequestData": str(act.context.workingDirectory / "LOGS"),
        "resultStatusType": "file",
        "resultStatusGetRequestData": str(act.context.workingDirectory / "LOGS/status.txt"),
        "monitorOnStart": [
            {
                "command": ["mkdir", ".\\LOGS"],
                "delayInSec": 0,
                "environmentVariables": {},
                "executeType": "targetCommand",
                "waitFinished": True,
                "workingDirectory": str(act.context.workingDirectory),
            },
            {
                "command": ["cmd.exe", "/c", "monitorOnStart.cmd"],
                "delayInSec": 0,
                "environmentVariables": {
                    "PROJECT_NAME": settings.PROJECT_NAME,
                    "VERSION": settings.VERSION,
                },
                "executeType": "targetCommand",
                "waitFinished": True,
                "workingDirectory": str(act.context.workingDirectory),
            },
            {
                "executeType": "request",
                "url": f"http://{settings.HOSTNAME_AND_PORT}/action/onstart",
                "method": "POST",
                "headers": HEADERS,
                "timeout": TEN_MINUTES_IN_MICROSECONDS,
            },
        ],
        "monitorOnStop": [
            {
                "command": ["powershell.exe", "-ExecutionPolicy", "Bypass", "-f", "./monitorOnStop.ps1"],
                "delayInSec": 0,
                "environmentVariables": {
                    "PROJECT_NAME": settings.PROJECT_NAME,
                    "VERSION": settings.VERSION,
                },
                "executeType": "targetCommand",
                "waitFinished": True,
                "workingDirectory": str(act.context.workingDirectory),
            },
            {
                "executeType": "request",
                "url": f"http://{settings.HOSTNAME_AND_PORT}/action/onstop",
                "method": "POST",
                "headers": HEADERS,
                "timeout": TEN_MINUTES_IN_MICROSECONDS,
            },
        ],
        "onAbort": [
            {
                "command": ["powershell.exe", "-ExecutionPolicy", "Bypass", "-f", "./onAbort.ps1"],
                "delayInSec": 0,
                "environmentVariables": {},
                "executeType": "targetCommand",
                "waitFinished": True,
                "workingDirectory": str(act.context.workingDirectory),
            },
            {
                "executeType": "request",
                "url": f"http://{settings.HOSTNAME_AND_PORT}/action/onabort",
                "method": "POST",
                "headers": HEADERS,
                "data": {"example_extra_data": "for_onabort"},
                "timeout": TEN_MINUTES_IN_MICROSECONDS,
            },
        ],
    }
    logging.debug(f"ACT Response: {response}")
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


@router.post("/monitor/target")
@log_wrapper
async def monitor_target(payload: models.MyActionCallbackModel):
    logging.info("=============================================================")
    logging.info("[Step] POST /monitor/target")

    try:
        result = await execute_ps1_on_remote(payload.act, payload.act.context.workingDirectory / "monitorTargetData.ps1", check=False)
    except UutConnectionError:
        logging.debug("Failed to connect to UUT")
        return {"result": True}

    if result.returncode == 0:
        # process exist -> running
        logging.info("[Step] POST /monitor/target process is running")
        return {"result": False}

    logging.info("[Step] POST /monitor/target process not found")
    return {"result": True}
