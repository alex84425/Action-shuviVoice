import asyncio
import datetime
import json
import logging

import static
from app.action import models
from app.action.models import MyActionPostModel
from app.config import get_settings
from fastapi import HTTPException, status
from tenacity import retry, stop_after_delay, wait_fixed
from vcosmosapiclient.api import MonitorFileResponse
from vcosmosapiclient.api_proxy import (
    execute_on_remote,
    send_file_to_remote,
    send_string_to_remote,
)
from vcosmosapiclient.library.rebootapi import force_reboot_once
from vcosmosapiclient.library.result import action_terminated
from vcosmosapiclient.utils import validator

settings = get_settings()

TWENTY_SECONDS = datetime.timedelta(seconds=20).seconds
FIVE_MINUTES_IN_SECONDS = datetime.timedelta(minutes=5).seconds
TEN_MINUTES_IN_MICROSECONDS = datetime.timedelta(minutes=10).seconds * 1000


async def execute_action(act: MyActionPostModel):

    # Sample code for direct pass
    if act.actionData.data.MyTestData == "PASS":
        raise validator.DirectStatusPass("test passed")

    # Sample code for direct fail
    if act.actionData.data.MyTestData == "FAIL":
        raise RuntimeError("test failed")

    # Sample code for most use case

    # 1. do some pre condition check, which will not create background process
    # send string to remote
    data_from_atc = act.actionData.data.dict()
    logging.info(data_from_atc)
    remote_path = act.context.workingDirectory / "LOGS" / "ResultDetails.json"
    await send_string_to_remote(act.target, json.dumps(data_from_atc, indent=4), remote_path)

    # send file to remote
    await send_file_to_remote(
        act.target, file_path=static.file("__init__.py"), remote_path=act.context.workingDirectory / "LOGS", override=True, timeout=60
    )

    # execute on remote
    await execute_on_remote(
        act.target,
        command=["echo", "Hello", ">", str(act.context.workingDirectory / "LOGS" / "hello.txt")],
        working_directory=act.context.workingDirectory,
    )

    response = MonitorFileResponse(
        task_folder=act.context.workingDirectory,
        monitor_file="LOGS/status.txt",
        result_file="LOGS/ResultDetails.json",
        status_file="LOGS/status.txt",
    ).dict()

    # example of onStart and onStop callback
    response["monitorOnStart"] = [
        {
            "executeType": "targetCommand",
            "environmentVariables": {},
            "workingDirectory": str(act.context.workingDirectory),
            "waitFinished": True,
            "command": ["powershell.exe", "echo", "start", ">", "_start.log"],
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
    ]

    # example of onAbort callback
    response["onAbort"] = [
        {
            "executeType": "request",
            "url": f"http://{settings.HOSTNAME_AND_PORT}/action/onabort",
            "method": "POST",
            "headers": {"Content-type": "application/json"},
            "data": act.dict(),
            "timeout": TEN_MINUTES_IN_MICROSECONDS,
        },
    ]

    # 2. create background task with name
    task = asyncio.create_task(execute_task(act, response))
    task.set_name(str(act.context.workingDirectory))
    return response


async def action_task(act: models.MyActionPostModel):
    logging.debug(f"action_task got {act=}")

    # Add your code here
    logging.debug("sleep 60 seconds for test abort")
    await asyncio.sleep(60)
    logging.debug("wake up")

    # generate monitor file
    remote_path = act.context.workingDirectory / "LOGS" / "status.txt"
    await send_string_to_remote(act.target, "PASS", remote_path)

    return "success"


async def execute_task(act: models.MyActionPostModel, response: dict):
    """
    Usage asyncio.create_task(executor.execute_task(act, response))
    generate monitor file and the result file based on the response's paths
    """
    try:
        ret = await action_task(act)
    except Exception as e:
        logging.exception("Action got exception: %s", e)
        await action_terminated(act, response, is_failed=True, reason=str(e))
    else:
        await action_terminated(act, response, is_failed=False, reason=ret)


@retry(reraise=True, stop=stop_after_delay(FIVE_MINUTES_IN_SECONDS), wait=wait_fixed(TWENTY_SECONDS))
async def onabort(act: MyActionPostModel):
    logging.debug(f"Aborting UUT {act.target.ip=}")
    task_name = str(act.context.workingDirectory)

    for task in asyncio.all_tasks():
        if task.get_name() == task_name and not task.done():
            try:
                logging.debug("Cancel task")
                task.cancel()
                break
            except asyncio.CancelledError:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"task is cancelled {task_name=}",
                )

    await force_reboot_once(act)
    remote_path = str(act.context.workingDirectory / "aborted.log")
    await send_string_to_remote(act.target, "aborted", remote_path, override=True)
    return {"status": "ok"}
