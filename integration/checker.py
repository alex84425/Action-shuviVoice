# this is a cli tool, which can be used to check the correctness of the feature test
import argparse
import asyncio
import json
import os

import httpx

JOB_MAGIC_INDEX = 0
TASKS_MAGIC_INDEX = 0


async def main():
    # print env variables
    print("ENV variables :")

    # source_version = os.environ["SourceVersion"]
    # repository_name = os.environ["RepositoryName"]
    vcosmos_token = os.environ.get("VCOSMOS_TOKEN")
    github_status = os.environ.get("GITHUB_STATUS")
    vcosmos_access_host = os.environ.get("VCOSMOS_ACCESS_HOST")
    hp_web_proxy = os.environ.get("HP_WEB_PROXY")

    print(vcosmos_token, github_status, vcosmos_access_host, hp_web_proxy)

    # get payload
    parser = argparse.ArgumentParser(description="Feature Test Checker")
    parser.add_argument("payload", type=str, help="ATC task done subscription callback payload")

    args = parser.parse_args()
    valid_json_data = args.payload.replace("'", '"')
    workflow_payload = json.loads(valid_json_data)

    job_id = workflow_payload["task_jobid"]
    get_job_url = f"https://{vcosmos_access_host}/api/v2/jobs/{job_id}"

    headers = {
        "accept": "application/json",
        "content-type": "application/json;charset=utf-8",
        "Authorization": vcosmos_token,
    }
    job_res = httpx.get(get_job_url, headers=headers, proxies=hp_web_proxy)
    print(job_res.status_code)
    if job_res.status_code != 200:
        raise Exception("job_res.status_code is not 200")
    job_data = job_res.json()
    job_status = job_data[JOB_MAGIC_INDEX]["status"]
    if "Terminated" == job_status:
        print("Not Implement: Terminated")

    if "Completed" == job_status:
        task_id = job_data[JOB_MAGIC_INDEX]["tasks"][TASKS_MAGIC_INDEX]["taskId"]
        get_task_url = f"https://{vcosmos_access_host}/api/v2/tasks/{task_id}"
        task_res = httpx.get(get_task_url, headers=headers, proxies=hp_web_proxy)
        if task_res.status_code != 200:
            raise Exception("task_res.status_code is not 200")

        task_data = task_res.json()
        task_status = task_data["status"]

        if task_status in ("Aborted", "Rejected"):
            print("Not Implement: Aborted, Rejected")

        if task_status == "Done":
            print("Not Implement: Done")


if __name__ == "__main__":
    asyncio.run(main())
