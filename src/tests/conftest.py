import binascii
import copy
import json
import os
import time
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.main import app

with open(Path(__file__).with_name("test_payload.json"), encoding="utf-8") as f:
    PAYLOAD = json.load(f)


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="module")
def async_app_client():
    client = AsyncClient(app=app, base_url="http://127.0.0.1:8080")
    yield client


@pytest.fixture(scope="function")
def act_raw():
    return PAYLOAD


def generate_taskid() -> str:
    timestamp = int(time.time())
    rest = binascii.b2a_hex(os.urandom(8)).decode("ascii")
    return f"{timestamp:x}{rest}"


def generate_working_directory(taskid: str) -> str:
    return f"c:/TestAutomation/TestJobs/{taskid}/00_ActionName_undefined_undefined"


def generate_act_payload() -> dict:
    """
    Generate ACT payload from test_payload.json.
    But replace taskId, and workingDirectory dynamically.
    """
    payload = copy.deepcopy(PAYLOAD)
    taskid = generate_taskid()
    payload["task"]["taskId"] = taskid
    payload["context"]["workingDirectory"] = generate_working_directory(taskid)
    return payload
