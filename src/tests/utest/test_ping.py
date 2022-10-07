import pytest
from fastapi import HTTPException, status
from pytest_httpx import HTTPXMock


def test_hello(test_app):
    response = test_app.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == status.HTTP_200_OK


def test_health_normal(test_app, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", status_code=404)
    response = test_app.get("/action/health")
    assert response.status_code == status.HTTP_200_OK


async def test_health_uut_exception(test_app, httpx_mock: HTTPXMock):
    httpx_mock.add_exception(HTTPException)
    with pytest.raises(HTTPException, match=r"fail to access UUT Proxy"):
        await test_app.get("/action/health")


async def test_health_not_404_response(test_app, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", status_code=400)
    with pytest.raises(HTTPException, match=r"Unexpected response from UUT proxy"):
        await test_app.get("/action/health")


def test_info(test_app):
    response = test_app.get("/action/info")
    assert response.status_code == status.HTTP_200_OK
