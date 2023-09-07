"""This module contains some mandatory endpoints.

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""

import logging

from fastapi import APIRouter, HTTPException, status
from vcosmosapiclient import errors
from vcosmosapiclient.api_proxy import execute_ps1_on_remote
from vcosmosapiclient.custom_logging import log_wrapper
from vcosmosapiclient.utils import validator

from app.action import executor, models

router = APIRouter()


@router.post("/act")
@validator.post
async def post_to_action(act: models.MyActionPostModel):
    if act.actionData.daemonMode:
        response = await executor.act_daemon_action(act)
    else:
        response = await executor.act_main_action(act)
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
    if payload.act.actionData.daemonMode:
        return {"result": True}

    # main mode
    result = False
    try:
        response = await execute_ps1_on_remote(payload.act, payload.act.context.workingDirectory / "isRunning.ps1", check=False)
        logging.debug(f"monitor response: {response}")
    except errors.UutConnectionError:
        logging.debug("Failed to connect to UUT")
    except errors.CommandError:
        logging.debug("Got CommandError")
    except errors.StatusCodeError:
        logging.debug("Got StatusCodeError")
    else:
        if response.returncode != 0:
            logging.debug("Stop watching")
            result = True

    return {"result": result}
