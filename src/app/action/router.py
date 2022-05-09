# -*- coding: utf-8 -*-
"""
This module contains some mandatory endpoints

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""


import json
import logging
from pathlib import Path

import aiofiles
from app.action import models
from app.config import Settings, get_fake_settings, get_settings
from fastapi import APIRouter, Depends
from vcosmosapiclient.api import MonitorFileResponse
from vcosmosapiclient.api_proxy import execute_on_remote, send_file_to_remote
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
    # Sample code for direct pass
    if act.actionData.data.MyTestData == "PASS":
        raise validator.DirectStatusPass("test passed")

    # Sample code for direct fail
    if act.actionData.data.MyTestData == "FAIL":
        raise RuntimeError("test failed")

    # Sample code for most use case
    data_from_atc = act.actionData.data.dict()
    logging.info(data_from_atc)
    async with aiofiles.tempfile.TemporaryDirectory() as d:
        result_path = Path(d, "ResultDetails.json")
        async with aiofiles.open(result_path, mode="w", encoding="utf-8") as f:
            await f.write(json.dumps(data_from_atc, indent=4))
        await send_file_to_remote(
            act.target, file_path=result_path, remote_path=act.context.workingDirectory / "LOGS", override=True, timeout=60
        )

    # execute on remote
    await execute_on_remote(
        act.target,
        command=["echo", "PASS", ">", str(act.context.workingDirectory / "LOGS" / "status.json")],
        working_directory=act.context.workingDirectory,
    )

    body = MonitorFileResponse(
        task_folder=act.context.workingDirectory,
        monitor_file="LOGS/status.json",
        result_file="LOGS/ResultDetails.json",
        status_file="LOGS/status.json",
    ).dict()
    return body
