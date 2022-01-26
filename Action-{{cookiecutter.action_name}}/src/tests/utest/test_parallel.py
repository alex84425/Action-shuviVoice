# -*- coding: utf-8 -*-
import asyncio
import logging

import pytest
from app.config import get_fake_settings, get_settings
from app.main import app
from httpx import AsyncClient
from vcosmosapiclient.depends import ApiDepends, FakeDepends


@pytest.mark.asyncio
async def test_parallel_act():
    FakeDepends.bios.fake_return["get_bios_on_remote"] = {
        "Manufacturing Programming Mode": "Lock",
        "Serial Number": "0123456789",
        "Universally Unique Identifier (UUID)": "11111111112222222222333333333344",
    }

    app.dependency_overrides[ApiDepends] = FakeDepends
    app.dependency_overrides[get_settings] = get_fake_settings

    client_number = 100

    act_list = []
    for i in range(client_number):
        act_list.append(
            {
                "context": {
                    "environmentVariables": {},
                    "parameters": {},
                    "actionResults": ["string"],
                    "workingDirectory": "C:\\TestAutomation\\53456575542",
                },
                "target": {
                    "ip": "15.36.158.55",
                    "port": "string",
                    "protocol": "string",
                    "serialNumber": "string",
                    "configuration": {},
                    "ssh": {},
                },
                "task": {"taskId": f"{i:08}"},
                "actionData": {
                    "type": "string",
                    "version": "string",
                    "data": {"test": "string"},
                    "index": 0,
                    "haltOnError": False,
                },
            }
        )

    async with AsyncClient(app=app, base_url="http://test") as ac:
        tasks = []
        for i in range(client_number):
            tasks.append(ac.post("/action/act", json=act_list[i]))

        results = await asyncio.gather(*tasks, return_exceptions=True)

    for response in list(results):
        logging.info(response)
        assert response.status_code == 200
        assert not response.json().get("errorOccurRequestData", None)
