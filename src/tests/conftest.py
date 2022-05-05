# -*- coding: utf-8 -*-
import json
from pathlib import Path

import pytest
from app.main import app
from starlette.testclient import TestClient

with open(Path(__file__).with_name("test_payload.json")) as f:
    PAYLOAD = json.load(f)


@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client


@pytest.fixture(scope="function")
def act_raw():
    return PAYLOAD
