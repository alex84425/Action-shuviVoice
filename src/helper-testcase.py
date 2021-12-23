# -*- coding: utf-8 -*-
import uuid

import requests

# from app.api.models import ActionModel, Target, Task, TestCaseModel
from custom_logging import CustomizeLogger

logger = CustomizeLogger.make_logger()

url = "http://127.0.0.1:8000"
testcase_endpoint = f"{url}/action/act"


uut_target = {"ip": "15.36.157.12"}
task = {"taskId": str(uuid.uuid4())}
ping_uut = {
    "guid": "2a86dc11-66f4-4ccb-87d3-74cf4d348531",
    "version": "1.0.0",
}

bios_flash = {
    "guid": "2a86dc11-66f4-4ccb-87d3-74cf4d348531",
    "version": "1.0.0",
}

act = {
    "target": uut_target,
    "task": task,
    "actionData": ping_uut,
}

# tatget: Target = Target(uut_ip)
# task: Task = Task(uuid.uuid4())
# testcase: TestCaseModel = TestCaseModel(**ping_uut)
# act: ActionModel = ActionModel(tatget, task, testcase)
logger.info(act)

if __name__ == "__main__":
    response = requests.post(url=testcase_endpoint, json=act)
    logger.info(response.json())
