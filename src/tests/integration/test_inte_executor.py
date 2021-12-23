# -*- coding: utf-8 -*-
# FIXME some code is no longer necessary in this action
import json
import logging
import os
import shutil
from pathlib import Path

import pytest
import requests

from app.core import executor

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
AF_URL = "https://vcosmos.hpcloud.hp.com/api/v1/AF"

testcase_tmp_path = Path(BASE_DIR, "testcases")

logger = logging.getLogger(__name__)


def setup_module():
    try:
        os.mkdir(testcase_tmp_path)
    except OSError:
        logger.debug("Creation of the directory %s failed" % testcase_tmp_path)
    else:
        logger.debug(
            "Successfully created the directory %s " % testcase_tmp_path
        )


def teardown_module():
    if os.path.exists(testcase_tmp_path):
        shutil.rmtree(testcase_tmp_path)


@pytest.fixture()
def presignurl_payload():
    filename = Path(BASE_DIR, "presignurl.json")
    with open(filename) as json_file:
        obj = json.load(json_file)
        return obj


def presignurl_api_endpint(
    af_url: str, guid: str, version: str, type: str = "testCase"
):
    base_url = "{af_url}/{type}/guid/{guid}/{version}/presignedDownloadUrl"
    url = base_url.format(af_url=af_url, type=type, guid=guid, version=version)
    return url


@pytest.fixture
def presignurl_testcase_live():
    guid = "2a86dc11-66f4-4ccb-87d3-74cf4d348531"
    version = "1.0.0"

    url = presignurl_api_endpint(af_url=AF_URL, guid=guid, version=version)
    response = requests.get(url=url)
    response_data = response.json()
    return response_data


@pytest.fixture
def presignurl_resource_live():
    guid = "9d21ba06-2d85-422e-a75d-58d51dcbbba9"
    version = "1.0.0-rc1"

    url = presignurl_api_endpint(
        af_url=AF_URL, guid=guid, version=version, type="resource"
    )
    response = requests.get(url=url)
    response_data = response.json()
    return response_data


@pytest.fixture
def testcase():
    obj = {
        "guid": "2a86dc11-66f4-4ccb-87d3-74cf4d348531",
        "version": "1.0.0",
    }
    return obj


@pytest.fixture
def resource():
    obj = {
        "guid": "9d21ba06-2d85-422e-a75d-58d51dcbbba9",
        "version": "1.0.0-rc1",
    }
    return obj


@pytest.mark.skip(reason="There is no such function in executor")
@pytest.mark.asyncio
async def test_get_testcase_path_from_af(testcase):
    expect_result = (
        "cdb5fc971969e2d6ecd9fe684360496049cb52f7f14a5e720bf122985b1dacc7"
    )
    expect_testname = "VCS_VCT_PingUUT"
    (
        response_data,
        response_status,
        response_name,
    ) = await executor.get_path_from_af(
        guid=testcase["guid"],
        version=testcase["version"],
    )

    assert response_status == 200
    assert response_name == expect_testname
    assert expect_result in response_data


@pytest.mark.asyncio
async def test_get_s3_presignurl(testcase):
    expect_result = (
        "cdb5fc971969e2d6ecd9fe684360496049cb52f7f14a5e720bf122985b1dacc7"
    )

    response_data, response_status = await executor.get_s3_presignurl(
        guid=testcase["guid"],
        version=testcase["version"],
    )

    assert response_status == 200
    assert expect_result in response_data


@pytest.mark.skip(reason="There is no such function in executor")
@pytest.mark.asyncio
async def test_get_testcase_file_from_af(
    presignurl_testcase_live: dict, monkeypatch
):
    filename = (
        "cdb5fc971969e2d6ecd9fe684360496049cb52f7f14a5e720bf122985b1dacc7.zip"
    )
    filedir = os.getcwd()
    presignedDownloadUrl = presignurl_testcase_live["presignedDownloadUrl"]

    estimated_filename = filename
    estimated_filepath = Path(filedir, filename)

    actual_filename, actual_filepath = await executor.get_file_from_af(
        presignedDownloadUrl=presignedDownloadUrl, filedir=filedir
    )

    assert estimated_filename == actual_filename
    assert estimated_filepath == actual_filepath

    # remove download files
    os.remove(actual_filepath)


@pytest.mark.skip(reason="There is no such function in executor")
@pytest.mark.asyncio
async def test_get_resource_path_from_af(resource):
    expect_result = (
        "196d2930670ea461ca642a913e98021305d88f69e934024261cf396e22643b54"
    )
    (
        response_data,
        response_status,
        response_name,
    ) = await executor.get_path_from_af(
        guid=resource["guid"],
        version=resource["version"],
        s3_type="resource",
    )

    assert response_status == 200
    assert expect_result in response_data


@pytest.mark.skip(reason="There is no such function in executor")
@pytest.mark.asyncio
async def test_get_s3_presignurl(resource):
    expect_result = (
        "196d2930670ea461ca642a913e98021305d88f69e934024261cf396e22643b54"
    )

    response_data, response_status = await executor.get_s3_presignurl(
        guid=resource["guid"], version=resource["version"], s3_type="resource"
    )

    assert response_status == 200
    assert expect_result in response_data


@pytest.mark.skip(reason="There is no such function in executor")
@pytest.mark.asyncio
async def test_get_resource_file_from_af(
    presignurl_resource_live: dict, monkeypatch
):
    filename = (
        "196d2930670ea461ca642a913e98021305d88f69e934024261cf396e22643b54.zip"
    )
    filedir = os.getcwd()
    presignedDownloadUrl = presignurl_resource_live["presignedDownloadUrl"]
    estimated_filename = filename
    estimated_filepath = Path(filedir, filename)
    actual_filename, actual_filepath = await executor.get_file_from_af(
        presignedDownloadUrl=presignedDownloadUrl, filedir=filedir
    )

    assert estimated_filename == actual_filename
    assert estimated_filepath == actual_filepath

    # remove download files
    os.remove(actual_filepath)
