# this is a cli tool, which can be used to check the correctness of the feature test
import argparse
import asyncio
import json
import os

import httpx


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
    response = httpx.get(get_job_url, headers=headers, proxies=hp_web_proxy)
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
