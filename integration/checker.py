# this is a cli tool, which can be used to check the correctness of the feature test
import argparse
import asyncio
import json
import logging
import os

import httpx
from feature_test.helper import BVT_TEST_CASES
from vcosmosapiclient.integration.atc_api_helper import ATC
from vcosmosapiclient.integration.feature_test_models import FeatureTestCase, ResultStatus, Task, TaskMode
from vcosmosapiclient.integration.github_helper import GitHubHelper, State

JOB_MAGIC_INDEX = 0
TASKS_MAGIC_INDEX = 0


class VCOSMOS_API:
    def __init__(self):
        self.base_url = os.environ["VCOSMOS_ACCESS_HOST"]
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json;charset=utf-8",
            "Authorization": os.environ["VCOSMOS_TOKEN"],
        }
        self.proxies = {
            "http://": "https://" + os.environ["HP_WEB_PROXY"],
            "https://": "https://" + os.environ["HP_WEB_PROXY"],
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
    # Fail if some env is not set
    print("ENV variables:")
    # actions_bot_token = os.environ["ACTIONS_BOT_TOKEN"]
    github_pat = os.environ["STATUS_GITHUB"]
    # vcosmos_token = os.environ["VCOSMOS_TOKEN"]
    print(github_pat)

    vcosmos_access_host = os.environ["VCOSMOS_ACCESS_HOST"]
    hp_web_proxy = os.environ["HP_WEB_PROXY"]
    print(vcosmos_access_host, hp_web_proxy)

    test_cases: list[FeatureTestCase] = BVT_TEST_CASES

    # get dispatch_parameters
    parser = argparse.ArgumentParser(description="Feature Test Checker")
    parser.add_argument("dispatch_parameters", type=str, help="ATC task done subscription callback dispatch_parameters")

    args = parser.parse_args()
    valid_json_data = args.dispatch_parameters.replace("'", '"')
    print(valid_json_data)
    # dispatch_parameters = json.loads(valid_json_data)
    # print(dispatch_parameters)

    # job_id = dispatch_parameters["job_id"]
    # test_name = dispatch_parameters["test_name"]
    # target_url = dispatch_parameters["target_url"]
    # source_version = dispatch_parameters["source_version"]
    # repository_name = dispatch_parameters["repository_name"]
    # print(job_id, test_name, target_url, source_version, repository_name)

    # github_helper: GitHubHelper = GitHubHelper(
    #     base_url="https://github.azc.ext.hp.com", repository_name=repository_name, source_version=source_version, pat=github_pat
    # )

    # # FIXME just use ATC and _monitor_task?
    # atc_helper = VCOSMOS_API()
    # job = await atc_helper.get_job(job_id)
    # job_status = job["status"]
    # task_id = job[JOB_MAGIC_INDEX]["tasks"][TASKS_MAGIC_INDEX]["taskId"]

    # task_result = await atc_helper.get_task(task_id)

    # if "Terminated" == job_status:
    #     await github_helper.update_status(
    #         state=State.FAILURE,
    #         target_url=target_url,
    #         description="task has been terminated",
    #         context=f"test/{test_name}",
    #     )

    # if "Completed" == job_status:
    #     for test_case in test_cases:
    #         if test_case.name == test_name:
    #             await testcase_result_checker_and_update_status(task_result, test_case, github_helper)

    # atc_helper = ATC(
    #     base_url_on_premise="",
    #     base_url_cloud=f"https://{vcosmos_access_host}",
    #     service_id=service_id,
    #     service_secret=service_secret,
    #     sitebroker=False,
    #     proxies={
    #         "http://": hp_web_proxy,
    #         "https://": hp_web_proxy,
    #     },
    # )

    # try:
    #     task = await atc_helper._monitor_task(job_id, timeout=60)
    # except Exception as exc:
    #     await github_helper.update_status(
    #         state=State.FAILURE,
    #         target_url=target_url,
    #         description=f"ERROR {exc}",
    #         context=f"test/{test_name}",
    #     )
    # else:
    #     for test_case in test_cases:
    #         if test_case.name == test_name:
    #             await testcase_result_checker_and_update_status(task, test_case, github_helper)


if __name__ == "__main__":
    asyncio.run(main())
