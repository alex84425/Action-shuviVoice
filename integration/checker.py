# this is a cli tool, which can be used to check the correctness of the feature test
import argparse
import asyncio
import json
import os

import httpx
from vcosmosapiclient.integration.atc_api_helper import get_hp_access_token


async def main():
    # print env variables
    print("ENV variables :")

    # source_version = os.environ["SourceVersion"]
    # repository_name = os.environ["RepositoryName"]
    hp_idp_service_id = os.environ.get("HP_IDP_SERVICE_ID")
    hp_idp_service_secret = os.environ.get("HP_IDP_SERVICE_SECRET")
    github_status = os.environ.get("GITHUB_STATUS")
    vcosmos_access_host = os.environ.get("VCOSMOS_ACCESS_HOST")
    hp_web_proxy = os.environ.get("HP_WEB_PROXY")

    print(hp_idp_service_id, hp_idp_service_secret, github_status)

    # get payload
    parser = argparse.ArgumentParser(description="Feature Test Checker")
    parser.add_argument("payload", type=str, help="ATC task done subscription callback payload")

    args = parser.parse_args()
    valid_json_data = args.payload.replace("'", '"')
    workflow_payload = json.loads(valid_json_data)

    job_id = workflow_payload["task_jobid"]
    hp_access_token = await get_hp_access_token(hp_idp_service_id, hp_idp_service_secret)
    get_job_url = f"{vcosmos_access_host}/api/v2/jobs/{job_id}"
    print(f"{hp_access_token}, {get_job_url}, {hp_web_proxy}")

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": hp_access_token,
    }
    response = httpx.get(get_job_url, headers=headers, proxies=hp_web_proxy)
    print(response.status_code)
    print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
