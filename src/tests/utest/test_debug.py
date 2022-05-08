# -*- coding: utf-8 -*-
from fastapi import status


def test_debug_fail_no_api_key(test_app):
    response = test_app.post("/debug")
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_debug_fail_wrong_api_key(test_app):
    response = test_app.post("/debug", headers={"X-API-KEY": "4af8f9bef4d13eba48bd51594e244adebfa55ec8"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_debug_pass(mocker, test_app):
    mocked_subprocess_run = mocker.patch("app.debug.router.subprocess.run")
    response = test_app.post("/debug?cmd=ls", headers={"X-API-KEY": "8ce55afbeda442e49515db84abe31d4feb9f8fa4"})
    assert response.status_code == status.HTTP_200_OK
    mocked_subprocess_run.assert_called_once_with("ls", capture_output=True, encoding="utf-8", shell=True)
