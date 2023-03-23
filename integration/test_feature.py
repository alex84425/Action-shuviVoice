import logging
import os
import re

import httpx
import pytest
from vcosmosapiclient.atc_api_helper import get_vcosmos_token

logging.getLogger().setLevel(logging.DEBUG)
ACTION_NAME = os.environ.get("actionNameLow")  # action-xxx


def get_action_name(root_name):
    # remove "action-"
    pattern = re.compile("^action-([a-z][a-z0-9]{2,20})$")
    matched = pattern.match(root_name)
    assert matched, "please check action name format"
    return matched.group(1)


async def get_env(key):
    "get_env_and_fail_if_none"
    value = os.environ.get(key)
    logging.debug("GET ENV %s is %s", key, value)
    if value is None:
        raise ValueError(f"{key} must not be None")
    return value


@pytest.mark.asyncio
@pytest.mark.parametrize("action_name", [ACTION_NAME])
async def test_testdev_feature_test(action_name):
    logging.debug("######################### trigger feature test #########################")
    assert action_name, "action_name is none, please set it"
    action_name_without_prefix = get_action_name(action_name)
    action_name_without_prefix = "providertemplate" if action_name_without_prefix == "executortemplate" else action_name_without_prefix

    if await get_env("ENV") != "dev":
        return "not dev site, skip"

    service_id = await get_env("HP_IDP_SERVICE_ID")
    service_secret = await get_env("HP_IDP_SERVICE_SECRET")
    host = await get_env("HOST_IP")
    port = await get_env("VCOSMOS_LOCAL_ENV_SITE_ENTRY_PORT")
    vcosmos_access_host = os.environ.get("VCOSMOS_ACCESS_HOST")
    atc_url = f"https://{host}:{port}"
    checker_url = f"https://{vcosmos_access_host}/api/action/{action_name_without_prefix}/checker"
    vcosmos_token = await get_vcosmos_token(atc_url, service_id, service_secret)

    response = httpx.post(
        checker_url,
        proxies={},
        verify=False,
        timeout=60,
        json={
            "CHECKER_URL": checker_url,
            "VCOSMOS_TOKEN": vcosmos_token,
            "VCOSMOS_ACCESS_HOST": vcosmos_access_host,
            "GITHUB_STATUS": os.environ.get("GITHUB_STATUS"),
            "SOURCEVERSION": os.environ.get("SourceVersion"),
            "REPOSITORYNAME": os.environ.get("RepositoryName"),
        },
    )
    logging.debug(f"response: {response.text}")
    if response.status_code != 200:
        raise ConnectionError(f"feature test trigger failed, status_code: {response.status_code}")
    return None
