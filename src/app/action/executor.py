import asyncio
import json
import logging
from pathlib import Path

import aiofiles
from app.action import models
from app.action.models import MyActionPostModel
from vcosmosapiclient.api import MonitorFileResponse
from vcosmosapiclient.api_proxy import (
    execute_on_remote,
    send_file_to_remote,
    send_string_to_remote,
)
from vcosmosapiclient.library.result import action_terminated
from vcosmosapiclient.utils import validator


async def execute_action(act: MyActionPostModel):

    # Sample code for direct pass
    if act.actionData.data.MyTestData == "PASS":
        raise validator.DirectStatusPass("test passed")

    # Sample code for direct fail
    if act.actionData.data.MyTestData == "FAIL":
        raise RuntimeError("test failed")

    # Sample code for most use case

    # === style 1 ===
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
        command=["echo", "PASS", ">", str(act.context.workingDirectory / "LOGS" / "status.txt")],
        working_directory=act.context.workingDirectory,
    )

    # === style 2 ===
    remote_path = act.context.workingDirectory / "LOGS" / "ResultDetails.json"
    await send_string_to_remote(act.target, json.dumps(data_from_atc, indent=4), remote_path)

    await asyncio.sleep(60)

    remote_path = act.context.workingDirectory / "LOGS" / "status.txt"
    await send_string_to_remote(act.target, "PASS", remote_path)

    body = MonitorFileResponse(
        task_folder=act.context.workingDirectory,
        monitor_file="LOGS/status.txt",
        result_file="LOGS/ResultDetails.json",
        status_file="LOGS/status.txt",
    ).dict()
    body["onAbort"] = [
        {
            "executeType": "targetCommand",
            "environmentVariables": {},
            "workingDirectory": str(act.context.workingDirectory),
            "waitFinished": True,
            "command": ["powershell.exe", "echo", "123", ">", "123.txt"],
        },
    ]
    body["monitorOnStart"] = [
        {
            "executeType": "request",
            "url": "http://action-executortemplate:8080/action/onstart",
            "method": "POST",
            "headers": {"Content-type": "application/json"},
            "data": {"mykey": "myvalue"},
            "timeout": 99999,
        },
    ]
    return body


async def action_task(act: models.MyActionPostModel):
    raise NotImplementedError("Add your code here")


async def execute_task(act: models.MyActionPostModel, response: dict):
    """
    Usage asyncio.create_task(executor.execute_task(act, ...))
    """
    try:
        ret = await action_task(act)
    except Exception as e:
        logging.exception("Action got exception: %s", e)
        await action_terminated(act, response, is_failed=True, reason=str(e))
    else:
        await action_terminated(act, response, is_failed=False, reason=ret)
