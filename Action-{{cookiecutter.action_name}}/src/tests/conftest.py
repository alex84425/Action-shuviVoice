# -*- coding: utf-8 -*-
import pytest_asyncio
from app.main import app
from starlette.testclient import TestClient


@pytest_asyncio.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client
