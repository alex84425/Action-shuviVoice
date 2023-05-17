# this is a cli tool, which can be used to check the correctness of the feature test
import argparse
import asyncio
import json
import logging
import os

import httpx
from feature_test.helper import INTEGRATION_TEST_CASES
from vcosmosapiclient.integration.feature_test_models import FeatureTestCase, ResultStatus, Task, TaskMode
from vcosmosapiclient.integration.github_helper import GitHubHelper, State

JOB_MAGIC_INDEX = 0
TASKS_MAGIC_INDEX = 0


class VCOSMOS_API:
    def __init__(self):
        self.base_url = os.environ.get("VCOSMOS_ACCESS_HOST")
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json;charset=utf-8",
            "Authorization": os.environ.get("VCOSMOS_TOKEN"),
        }
        self.proxies = {
            "http://": "https://" + os.environ.get("HP_WEB_PROXY", ""),
            "https://": "https://" + os.environ.get("HP_WEB_PROXY", ""),
        }

    async def get_job(self, job_id: str):
        async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies, verify=False, timeout=60) as client:
            get_job_url = f"https://{self.base_url}/api/v2/jobs/" + job_id
            job_res = await client.get(get_job_url)

        if job_res.status_code != 200:
            raise Exception("job_res.status_code is not 200")

        return job_res.json()

    async def get_task(self, task_id: str):
        async with httpx.AsyncClient(headers=self.headers, proxies=self.proxies, verify=False, timeout=60) as client:
            get_task_url = f"https://{self.base_url}/api/v2/tasks/{task_id}"
            task_res = await client.get(get_task_url)

        return task_res.json()


async def testcase_result_checker_and_update_status(task_res: dict, test_case: FeatureTestCase, github: GitHubHelper):
    print(f"{task_res=}")

    try:
        test_case.task = Task(task_res, mode=TaskMode.SUBSCRIPTION)
        await test_case.checker(test_case.task)
    except Exception as exc:
        msg = f"{exc.__class__.__name__!s:.40}: {exc!s:.100}"
        logging.debug(f"Checker: test_case FAIL ({msg})")
        test_case.result_details = f"❌({msg})"
        test_case.result_status = ResultStatus.FAIL
    else:
        logging.debug("Checker: test_case PASS")
        test_case.result_details = "✔"
        test_case.result_status = ResultStatus.PASS

    try:
        await github.update_status(
            state=State.SUCCESS if test_case.result_status == ResultStatus.PASS else State.FAILURE,
            target_url=test_case.job_link,
            description=test_case.result_details,
            context=f"test/{test_case.name}",
        )
    except Exception as exc:
        logging.error(f"update github status failed, (reason: {exc})")


async def main():
    # print env variables
    print("ENV variables :")
    github_pat = os.environ.get("ACTIONS_BOT_TOKEN", "")

    # get payload
    parser = argparse.ArgumentParser(description="Feature Test Checker")
    parser.add_argument("payload", type=str, help="ATC task done subscription callback payload")

    args = parser.parse_args()
    valid_json_data = args.payload.replace("'", '"')
    workflow_payload = json.loads(valid_json_data)

    job_id = workflow_payload["task_jobid"]
    source_version = workflow_payload["source_version"]
    repository_name = workflow_payload["repository_name"]
    target_url = workflow_payload["target_url"]
    test_name = workflow_payload["test_name"]

    print(source_version, repository_name)

    github_helper: GitHubHelper = GitHubHelper(
        base_url="https://github.azc.ext.hp.com", repository_name=repository_name, source_version=source_version, pat=github_pat
    )

    vcosmos_api = VCOSMOS_API()
    job = await vcosmos_api.get_job(job_id)
    job_status = job["status"]
    task_id = job[JOB_MAGIC_INDEX]["tasks"][TASKS_MAGIC_INDEX]["taskId"]

    task_result = await vcosmos_api.get_task(task_id)

    if "Terminated" == job_status:
        await github_helper.update_status(
            state=State.FAILURE,
            target_url=target_url,
            description="task has been terminated",
            context=f"test/{test_name}",
        )

    if "Completed" == job_status:
        test_cases: list[FeatureTestCase] = INTEGRATION_TEST_CASES
        for test_case in test_cases:
            if test_case.name == test_name:
                await testcase_result_checker_and_update_status(task_result, test_case, github_helper)


if __name__ == "__main__":
    asyncio.run(main())
