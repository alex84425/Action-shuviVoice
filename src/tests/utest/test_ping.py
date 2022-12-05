import pytest
from fastapi import HTTPException, status
from pytest_httpx import HTTPXMock


@pytest.mark.asyncio
async def test_hello(async_app_client):
    response = await async_app_client.get("/")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.asyncio
async def test_ping(async_app_client):
    response = await async_app_client.get("/ping")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip(reason="wrong usage of httpx mock")
@pytest.mark.asyncio
async def test_health_normal(async_app_client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", status_code=404)
    response = await async_app_client.get("/action/health")
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.skip(reason="wrong usage of httpx mock")
@pytest.mark.asyncio
async def test_health_uut_exception(async_app_client, httpx_mock: HTTPXMock):
    httpx_mock.add_exception(HTTPException)
    with pytest.raises(HTTPException, match=r"fail to access UUT Proxy"):
        await async_app_client.get("/action/health")


@pytest.mark.skip(reason="wrong usage of httpx mock")
@pytest.mark.asyncio
async def test_health_not_404_response(async_app_client, httpx_mock: HTTPXMock):
    httpx_mock.add_response(method="GET", status_code=400)
    with pytest.raises(HTTPException, match=r"Unexpected response from UUT proxy"):
        await async_app_client.get("/action/health")


@pytest.mark.asyncio
async def test_info(async_app_client):
    response = await async_app_client.get("/action/info")
    assert response.status_code == status.HTTP_200_OK
