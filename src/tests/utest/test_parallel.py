import asyncio
import logging
from unittest.mock import AsyncMock

import pytest
from fastapi import status

from tests.conftest import generate_act_payload

CLIENT_NUMBER = 20
ACTION_ENDPOINT = "/action/onstart"


@pytest.mark.skip(reason="no such example")
@pytest.mark.asyncio
async def test_parallel_act_happy_path(mocker, async_app_client):
    mocked = AsyncMock(return_value="dummy")
    mocked_send_file_to_remote = mocker.patch("app.action.executor.send_file_to_remote", new_callable=AsyncMock)
    mocked_send_string_to_remote = mocker.patch("app.action.executor.send_string_to_remote", new_callable=AsyncMock)
    mocked_execute_on_remote = mocker.patch("app.action.executor.execute_on_remote", side_effect=mocked)
    mocker.patch("app.action.executor.asyncio.sleep")
    payload = generate_act_payload()

    tasks = [async_app_client.post(ACTION_ENDPOINT, json=payload) for _ in range(CLIENT_NUMBER)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for response in list(results):
        logging.debug(response)
        assert not response.json().get("errorOccurRequestData", None)
        assert response.status_code == status.HTTP_200_OK

    assert mocked_send_file_to_remote.call_count == CLIENT_NUMBER
    assert mocked_send_string_to_remote.call_count == CLIENT_NUMBER * 2
    assert mocked_execute_on_remote.call_count == CLIENT_NUMBER
