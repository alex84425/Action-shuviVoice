import logging
import os

import httpx
import pytest
from vcosmosapiclient.atc_api_helper import get_vcosmos_token

logging.getLogger().setLevel(logging.DEBUG)


async def get_env(key):
    "get_env_and_fail_if_none"
    value = os.environ.get(key)
    logging.debug("GET ENV %s is %s", key, value)
    if value is None:
        raise ValueError(f"{key} must not be None")
    return value


@pytest.mark.asyncio
async def test_smr_feature_test():
    logging.debug("######################### trigger feature test #########################")
    if await get_env("ENV") != "dev":
        return "not dev site, skip"

    service_id = await get_env("HP_IDP_SERVICE_ID")
    service_secret = await get_env("HP_IDP_SERVICE_SECRET")
    host = await get_env("HOST_IP")
    port = await get_env("VCOSMOS_LOCAL_ENV_SITE_ENTRY_PORT")
    atc_url = f"https://{host}:{port}"
    vcosmos_token = await get_vcosmos_token(atc_url, service_id, service_secret)

    response = httpx.post(
        f"{atc_url}/api/action/smr/checker",
        proxies={},
        verify=False,
        timeout=60,
        json={
            "VCOSMOS_TOKEN": vcosmos_token,
            "VCOSMOS_ACCESS_HOST": os.environ.get("VCOSMOS_ACCESS_HOST"),
            "GITHUB_STATUS": os.environ.get("GITHUB_STATUS"),
            "SOURCEVERSION": os.environ.get("SourceVersion"),
            "REPOSITORYNAME": os.environ.get("RepositoryName"),
        },
    )
    logging.debug(f"response: {response.text}")
    if response.status_code != 200:
        raise ConnectionError(f"feature test trigger failed, status_code: {response.status_code}")
