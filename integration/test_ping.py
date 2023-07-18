import logging
import os

import httpx
import pytest
import tenacity

logging.getLogger().setLevel(logging.DEBUG)
HOST_IP = os.environ.get("HOST_IP")
ACTION_NAME = os.environ.get("actionNameLow")  # action-xxx


@tenacity.retry(reraise=True, stop=tenacity.stop.stop_after_attempt(14), wait=tenacity.wait.wait_random_exponential(max=60))
@pytest.mark.parametrize("action_name", [ACTION_NAME])
def test_testdev_get_action_health_via_container_dns_expect_200ok(action_name):
    assert action_name, "action_name is none, please set it"

    url = f"http://{action_name}:8080/action/health"
    resp = httpx.get(url, proxies={}, timeout=10)
    logging.debug(f"{url=} {resp=} {resp.text=}")
    assert resp.status_code == 200


@tenacity.retry(reraise=True, stop=tenacity.stop.stop_after_attempt(8), wait=tenacity.wait.wait_random_exponential(max=60))
@pytest.mark.parametrize("action_name", [ACTION_NAME])
def test_testdev_get_action_health_via_nginx_expect_200ok(action_name):
    assert action_name, "action_name is none, please set it"
    assert HOST_IP, "HOST_IP is none, please set it"

    url = f"https://{HOST_IP}/{action_name}/action/health"
    resp = httpx.get(url, verify=False, proxies={}, timeout=10)
    logging.debug(f"{url=} {resp=} {resp.text=}")
    assert resp.status_code == 200
