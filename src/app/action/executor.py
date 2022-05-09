import json
import logging
from pathlib import Path

import aiofiles
from app.action.models import MyActionPostModel
from vcosmosapiclient.api import MonitorFileResponse
from vcosmosapiclient.api_proxy import execute_on_remote, send_file_to_remote
from vcosmosapiclient.utils import validator


async def execute(act: MyActionPostModel):

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
        command=["echo", "PASS", ">", str(act.context.workingDirectory / "LOGS" / "status.txt")],
        working_directory=act.context.workingDirectory,
    )

    body = MonitorFileResponse(
        task_folder=act.context.workingDirectory,
        monitor_file="LOGS/status.txt",
        result_file="LOGS/ResultDetails.json",
        status_file="LOGS/status.txt",
    ).dict()
    return body
