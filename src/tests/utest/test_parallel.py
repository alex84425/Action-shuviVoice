# -*- coding: utf-8 -*-
import asyncio
import logging
from unittest.mock import AsyncMock

import pytest
from fastapi import status
from tests.conftest import generate_act_payload

CLIENT_NUMBER = 100


@pytest.mark.asyncio
async def test_parallel_act_direct_pass(async_app_client):
    payload = generate_act_payload()
    payload["actionData"]["data"]["MyTestData"] = "PASS"

    tasks = [async_app_client.post("/action/act", json=payload) for _ in range(CLIENT_NUMBER)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for response in list(results):
        logging.info(response.text)
        assert response.status_code == status.HTTP_200_OK
        assert not response.json().get("errorOccurRequestData", None)
        assert response.json()["resultStatusGetRequestData"] == "PASS"


@pytest.mark.asyncio
async def test_parallel_act_direct_fail(async_app_client):
    payload = generate_act_payload()
    payload["actionData"]["data"]["MyTestData"] = "FAIL"

    tasks = [async_app_client.post("/action/act", json=payload) for _ in range(CLIENT_NUMBER)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for response in list(results):
        logging.info(response.text)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["errorOccurRequestData"]
        assert response.json()["resultStatusGetRequestData"] == "FAIL"


@pytest.mark.asyncio
async def test_parallel_act_happy_path(mocker, async_app_client):
    mocked = AsyncMock(return_value="dummy")
    mocked_send_file_to_remote = mocker.patch("app.action.router.send_file_to_remote", new_callable=AsyncMock)
    mocked_execute_on_remote = mocker.patch("app.action.router.execute_on_remote", side_effect=mocked)
    payload = generate_act_payload()

    tasks = [async_app_client.post("/action/act", json=payload) for _ in range(CLIENT_NUMBER)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for response in list(results):
        logging.debug(response)
        assert response.status_code == status.HTTP_200_OK
        assert not response.json().get("errorOccurRequestData", None)

    assert mocked_send_file_to_remote.call_count == CLIENT_NUMBER
    assert mocked_execute_on_remote.call_count == CLIENT_NUMBER
