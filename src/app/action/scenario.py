# -*- coding: utf-8 -*-
import json

from app.action import models
from app.log import atclogger as logger
from vcosmosapiclient.api import MonitorFileResponse


async def post_to_action_remote(postact: models.MyActionPostModel, dryrun=False):
    body = MonitorFileResponse(
        task_id=postact.task.taskId,
        monitor_file="LOGS/ResultDetails.json",
        result_file="LOGS/ResultDetails.json",
        status_file="LOGS/status.json",
    ).dict()

    logger.debug("post_to_action_remote output: %s", json.dumps(body))
    logger.debug("post_to_action_remote output: %s", json.dumps(body, indent=4))
    return body
