import logging
import os

import httpx
import pytest

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
HOST_IP = os.environ.get("HOST_IP")

ACTIONS = ["executortemplate"]



@pytest.mark.parametrize("action", ACTIONS)
def test_ping(action):
    logging.debug(f"{HOST_IP=}")
    assert HOST_IP, "HOST_IP is none, please set it"

    url = f"https://{HOST_IP}/action-{action}/ping"
    resp = httpx.get(url, verify=False, proxies={}, timeout=10)
    logging.debug(f"{url=} {resp=} {resp.text=}")
    assert resp.status_code == 200

