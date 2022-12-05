import logging
import os

import httpx

logging.getLogger().setLevel(logging.DEBUG)
HOST_IP = os.environ.get("HOST_IP")


def test_testdev_get_action_executortemplate_health_via_container_dns_expect_200ok():
    url = "http://action-executortemplate:8080/action/health"
    resp = httpx.get(url, proxies={}, timeout=10)
    logging.debug(f"{url=} {resp=} {resp.text=}")
    assert resp.status_code == 200


def test_testdev_get_action_executortemplate_health_via_nginx_expect_200ok():
    assert HOST_IP, "HOST_IP is none, please set it"

    url = f"https://{HOST_IP}/action-executortemplate/action/health"
    resp = httpx.get(url, verify=False, proxies={}, timeout=10)
    logging.debug(f"{url=} {resp=} {resp.text=}")
    assert resp.status_code == 200
