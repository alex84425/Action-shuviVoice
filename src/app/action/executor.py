import asyncio
import datetime
import json
import logging

from fastapi import HTTPException, status
from tenacity import retry
from tenacity.stop import stop_after_delay
from tenacity.wait import wait_fixed
from vcosmosapiclient.api_proxy import execute_on_remote, send_file_to_remote, send_string_to_remote
from vcosmosapiclient.library.rebootapi import force_reboot_once

import static
from app.action import models
from app.config import get_settings
from app.description import DESCRIPTION_DICT

settings = get_settings()

TWENTY_SECONDS = datetime.timedelta(seconds=20).total_seconds()
FIVE_MINUTES_IN_SECONDS = datetime.timedelta(minutes=5).total_seconds()


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

    await force_reboot_once(act)
    remote_path = act.context.workingDirectory / "aborted.log"
    await send_string_to_remote(act.target, "aborted", remote_path, override=True)
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
    data_from_atc = act.actionData.data.dict(by_alias=True)
    logging.info(data_from_atc)
    remote_path = act.context.workingDirectory / "LOGS" / "ResultDetails.json"

    await send_string_to_remote(act.target, json.dumps(data_from_atc, indent=4), remote_path)
    # send log_link contain action meta
    action_meta_remote_path = act.context.workingDirectory / "LOGS" / "action_meta.txt"
    action_meta = DESCRIPTION_DICT
    await send_string_to_remote(act.target, json.dumps(action_meta, indent=4), action_meta_remote_path, override=True)

    # send monitor file
    await send_file_to_remote(act.target, static.file("monitor_target.ps1"), act.context.workingDirectory, override=True)
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

    # 2. execute task
    logging.debug("sleep 10 seconds for test abort")
    await asyncio.sleep(10)
    logging.debug("wake up")

    # generate monitor file
    remote_path = act.context.workingDirectory / "LOGS" / "status.txt"
    await send_string_to_remote(act.target, "PASS", remote_path)

    return "success"
