# -*- coding: utf-8 -*-
from app.config import get_settings

SETTINGS = get_settings()


def test_hello(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"service": get_settings().PROJECT_NAME, "version": get_settings().VERSION}


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_health(test_app):
    response = test_app.get("/action/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_info(test_app):
    response = test_app.get("/action/info")
    assert response.status_code == 200
    assert response.json() == {"type": get_settings().PROJECT_NAME, "typeVer": get_settings().VERSION}
