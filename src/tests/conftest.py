# -*- coding: utf-8 -*-
import binascii
import copy
import json
import os
import time
from pathlib import Path

import pytest
from app.config import get_fake_settings, get_settings
from app.main import app
from httpx import AsyncClient
from starlette.testclient import TestClient

with open(Path(__file__).with_name("test_payload.json")) as f:
    PAYLOAD = json.load(f)


@pytest.fixture(scope="module")
def test_app():
    app.dependency_overrides[get_settings] = get_fake_settings
    client = TestClient(app)
    yield client
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
def async_app_client():
    app.dependency_overrides[get_settings] = get_fake_settings
    client = AsyncClient(app=app, base_url="http://test")
    yield client
    app.dependency_overrides = {}


@pytest.fixture(scope="function")
def act_raw():
    return PAYLOAD


def generate_taskid() -> str:
    timestamp = int(time.time())
    rest = binascii.b2a_hex(os.urandom(8)).decode("ascii")
    return f"{timestamp:x}{rest}"


def generate_act_payload() -> dict:
    payload = copy.deepcopy(PAYLOAD)
    payload["task"]["taskId"] = generate_taskid()
    return payload
