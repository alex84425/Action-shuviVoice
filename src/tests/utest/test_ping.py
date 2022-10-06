from fastapi import status
from pytest_httpx import HTTPXMock


def test_hello(test_app):
    response = test_app.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == status.HTTP_200_OK


def test_health_new(test_app, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", text="dummy test", status_code=404)
    response = test_app.get("/action/health")
    assert response.status_code == status.HTTP_200_OK


def test_info(test_app):
    response = test_app.get("/action/info")
    assert response.status_code == status.HTTP_200_OK
