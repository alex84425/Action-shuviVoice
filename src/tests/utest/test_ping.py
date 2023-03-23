import pytest
from fastapi import HTTPException, status
from pytest_httpx import HTTPXMock

from app.health import router


@pytest.mark.asyncio
async def test_hello(async_app_client):
    response = await async_app_client.get("/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_ping_route(async_app_client):
    response = await async_app_client.get("/ping")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_health_normal(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", status_code=404)
    response = await router.health()
    assert response == {"status": "ok"}


@pytest.mark.asyncio
async def test_health_uut_exception(httpx_mock: HTTPXMock):
    httpx_mock.add_exception(Exception())
    with pytest.raises(HTTPException) as exc_info:
        await router.health()
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert "fail to access UUT Proxy" in exc_info.value.detail


@pytest.mark.asyncio
async def test_health_not_404_response(httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", status_code=400)
    with pytest.raises(HTTPException) as exc_info:
        await router.health()
    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    assert "Unexpected response from UUT proxy" in exc_info.value.detail


@pytest.mark.asyncio
async def test_info(async_app_client):
    response = await async_app_client.get("/action/info")
    assert response.status_code == status.HTTP_200_OK
