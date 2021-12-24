# -*- coding: utf-8 -*-
def test_ping(test_app):
    response = test_app.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong!"}


def test_health(test_app):
    response = test_app.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_version(test_app):
    response = test_app.get("/version")
    assert response.status_code == 200
    assert "ENVIRONMENT" in response.json()
