# -*- coding: utf-8 -*-
import asyncio
import logging

from app.action import models
from app.config import get_settings
from fastapi import APIRouter
from vcosmosapiclient.api import MonitorFileResponse
from vcosmosapiclient.utils import validator

router = APIRouter()


@router.get("/info")
async def info():
    """
    Required endpoint
    https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract
    """  # noqa
    return {"type": get_settings().PROJECT_NAME, "typeVer": get_settings().VERSION}


@router.get("/health")
async def health():
    """
    Required endpoint
    https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract
    """  # noqa
    return {"status": "ok"}


@router.post("/dryrun")
@validator.post
async def post_to_action_dryrun(act: models.MyActionPostModel):
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
    raise body


@router.post("/act")
@validator.post
async def post_to_action(act: models.MyActionPostModel):
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

    logging.info("this is template /action/act")
    raise body
