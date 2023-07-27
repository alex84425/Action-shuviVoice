import asyncio
import datetime
import json
import logging
from pathlib import Path

from fastapi import HTTPException, status
from tenacity import retry
from tenacity.stop import stop_after_delay
from tenacity.wait import wait_fixed
from vcosmosapiclient import static as submodule_static
from vcosmosapiclient.api_proxy import (
    execute_on_remote,
    execute_ps1_on_remote,
    extract_zip_to_remote,
    send_file_to_remote,
    send_file_to_remote_rename,
    send_string_to_remote,
)
from vcosmosapiclient.errors import UutConnectionError

import static
from app.action import models
from app.config import get_settings
from app.description import DESCRIPTION_DICT

settings = get_settings()

HEADERS = {"Content-type": "application/json"}
TWENTY_SECONDS = datetime.timedelta(seconds=20).total_seconds()
FIVE_MINUTES_IN_SECONDS = datetime.timedelta(minutes=5).total_seconds()
TEN_MINUTES_IN_MICROSECONDS = int(datetime.timedelta(minutes=10).total_seconds() * 1000)  # for axios


@retry(reraise=True, stop=stop_after_delay(FIVE_MINUTES_IN_SECONDS), wait=wait_fixed(TWENTY_SECONDS))
async def onabort(act: models.MyActionPostModel):
    logging.debug("Aborting UUT IP: %s", act.target.ip)
    task_name = str(act.context.workingDirectory)

    for task in asyncio.all_tasks():
        if task.get_name() == task_name and not task.done():
            try:
                logging.debug("Cancel task")
                task.cancel()
                break
            except asyncio.CancelledError as exc:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"task is cancelled {task_name=}",
                ) from exc

    try:
        await execute_ps1_on_remote(act, act.context.workingDirectory / "onAbort.ps1", check=False)
        await send_string_to_remote(act.target, "aborted", act.context.workingDirectory / "aborted.log", override=True)
    except UutConnectionError as exc:
        logging.debug("Abort fail to connect to UUT")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"Fail to connect to UUT: {exc}",
        ) from exc

    return {"status": "ok"}


async def onstart(act: models.MyActionPostModel):
    logging.debug("OnStart action on UUT %s", act.target.ip)
    task = asyncio.create_task(execute_action(act))
    task.set_name(str(act.context.workingDirectory))
    await task
    return {"status": "ok"}


async def onstop(act: models.MyActionPostModel):
    logging.debug("OnStop action on UUT %s", act.target.ip)
    return {"status": "ok"}


async def execute_action(act: models.MyActionPostModel):
    logging.debug("action_task got act=%s", act)

    # 1. do some pre condition check, which will not create background process
    # send string to remote
    data_from_atc = act.actionData.data.dict(by_alias=False)
    logging.info(data_from_atc)
    remote_path = act.context.workingDirectory / "LOGS" / "result.txt"

    await send_string_to_remote(act.target, json.dumps(data_from_atc, indent=4), remote_path)
    # send log_link contain action meta
    action_meta_remote_path = act.context.workingDirectory / "LOGS" / "action_meta.txt"
    action_meta = DESCRIPTION_DICT
    await send_string_to_remote(act.target, json.dumps(action_meta, indent=4), action_meta_remote_path, override=True)

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

    # generate monitor file
    remote_path = act.context.workingDirectory / "LOGS" / "status.txt"
    await send_string_to_remote(act.target, "PASS", remote_path)

    return "success"


async def act_main_action(act: models.MyActionPostModel):
    # send action files
    await extract_zip_to_remote(act.target, static.file("examples.zip"), remote_path=act.context.workingDirectory)

    return {
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


def target_command_ps1(act: models.MyActionPostModel, script_file, env=None, wait=True):
    filename = Path(script_file).stem
    command = [
        "powershell.exe",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        f".\\{script_file}",
        f">>LOGS\\{filename}.log",
        "2>&1",
    ]
    return {
        "executeType": "targetCommand",
        "environmentVariables": env if env else {},
        "workingDirectory": str(act.context.workingDirectory),
        "waitFinished": wait,
        "command": command,
    }


async def act_daemon_action(act: models.MyActionPostModel):
    default_execution_time_limit = FIVE_MINUTES_IN_SECONDS

    # send action files
    if not act.actionData.daemonMode:
        raise RuntimeError("Something wrong of model mapping")

    if not isinstance(act.actionData.data, (models.DaemonPageOneModel, models.DaemonPageTwoModel)):
        raise RuntimeError("Something wrong of model mapping")

    await extract_zip_to_remote(act.target, static.file("daemon_examples.zip"), remote_path=act.context.workingDirectory)

    # send broken daemon.ps1 if checkbox is checked (for test negative case)
    if act.actionData.data.Operation == models.DaemonOperationEnum.OPERATION_1 and act.actionData.data.check_box:
        remote_file_path = act.context.workingDirectory / "daemon.ps1"
        await send_file_to_remote_rename(act.target, static.file("daemon_broken.ps1"), full_remote_path=remote_file_path)
    else:
        await send_file_to_remote(act.target, static.file("daemon.ps1"), remote_path=act.context.workingDirectory)

    # send libs from submodule
    await send_file_to_remote(act.target, submodule_static.get_file("TaskScheduler.ps1"), remote_path=act.context.workingDirectory)

    # send parameters
    parameters_json_path = act.context.workingDirectory / "parameters.json"
    parameters = act.actionData.data.dict()
    await send_string_to_remote(act.target, json.dumps(parameters, indent=4), parameters_json_path, override=True)

    # create log folder
    log_folder = act.context.workingDirectory / "LOGS"
    await execute_on_remote(act.target, ["mkdir", str(log_folder)], act.context.workingDirectory)

    result_flag = log_folder / "result.txt"
    status_flag = log_folder / "status.txt"
    return {
        "monitorType": "exist",
        "monitorTargetType": "file",
        "monitorTargetData": str(result_flag),
        "monitorBehavior": "stop",
        "monitorIntervalInSecs": 60,
        "monitorTimeoutInSecs": default_execution_time_limit,
        "resultType": "file",
        "resultGetRequestData": str(result_flag),
        "storeType": "file",
        "storeGetRequestData": str(log_folder),
        "resultStatusType": "file",
        "resultStatusGetRequestData": str(status_flag),
        "monitorOnStart": [target_command_ps1(act, "monitorOnStart.ps1")],
        "monitorOnStop": [target_command_ps1(act, "monitorOnStop.ps1")],
        "onAbort": [target_command_ps1(act, "onAbort.ps1")],
    }
