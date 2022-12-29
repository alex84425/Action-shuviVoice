import logging
import os

import httpx
import pytest

logging.getLogger().setLevel(logging.DEBUG)
HOST_IP = os.environ.get("HOST_IP")
ACTION_NAME = os.environ.get("actionNameLow")  # action-xxx
assert HOST_IP, "HOST_IP is none, please set it"
assert ACTION_NAME, "ACTION_NAME is none, please set it"


@pytest.mark.parametrize("action_name", [ACTION_NAME])
def test_testdev_get_action_health_via_container_dns_expect_200ok(action_name):
    url = f"http://{action_name}:8080/action/health"
    resp = httpx.get(url, proxies={}, timeout=10)
    logging.debug(f"{url=} {resp=} {resp.text=}")
    assert resp.status_code == 200


@pytest.mark.parametrize("action_name", [ACTION_NAME])
def test_testdev_get_action_health_via_nginx_expect_200ok(action_name):
    url = f"https://{HOST_IP}/{action_name}/action/health"
    resp = httpx.get(url, verify=False, proxies={}, timeout=10)
    logging.debug(f"{url=} {resp=} {resp.text=}")
    assert resp.status_code == 200
