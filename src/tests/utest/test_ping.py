# -*- coding: utf-8 -*-
from app.config import get_settings
from fastapi import status

SETTINGS = get_settings()


def test_hello(test_app):
    response = test_app.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == status.HTTP_200_OK


def test_health(test_app):
    response = test_app.get("/action/health")
    assert response.status_code == status.HTTP_200_OK


def test_info(test_app):
    response = test_app.get("/action/info")
    assert response.status_code == status.HTTP_200_OK
