# -*- coding: utf-8 -*-
# FIXME some code is no longer necessary in this action
import json

import pytest

from app.api.api_v1.endpoints import action


@pytest.mark.skip(reason="There is no such function in action")
def test_router_platform(test_app, monkeypatch):
    test_platform_payload = {"platform_name": "Linden13", "milestone": None}

    expected_response = {"softpaqs": {"list1": "test"}}

    async def mock_get_platform_result(platform_name, mile_stone_date):
        return {"list1": "test"}

    monkeypatch.setattr(action, "get_platform_result", mock_get_platform_result)

    response = test_app.post(
        "/api/action/info/smr/action/veteran/platform",
        data=json.dumps(test_platform_payload),
    )

    assert response.status_code == 200
    assert response.json() == expected_response
