# -*- coding: utf-8 -*-
from app.core.config import get_settings

settings = get_settings()

def test_ping(test_app):
    response = test_app.get(f"{settings.API_V1_STR}/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_hello(test_app):
    response = test_app.get(f"{settings.API_V1_STR}/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_health(test_app):
    response = test_app.get(f"{settings.API_V1_STR}/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version(test_app):
    response = test_app.get(f"{settings.API_V1_STR}/version")
    assert response.status_code == 200
    assert "ENVIRONMENT" in response.json()
    assert "AF_URL" in response.json()
