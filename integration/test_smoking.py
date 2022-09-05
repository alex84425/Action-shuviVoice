import base64
import logging
import os

import httpx


def get_atc_url():
    HOST_IP = os.environ.get("HOST_IP")
    VCOSMOS_LOCAL_ENV_SITE_ENTRY_PORT = os.environ.get("VCOSMOS_LOCAL_ENV_SITE_ENTRY_PORT")
    assert HOST_IP, "HOST_IP is none, please check env var"
    assert VCOSMOS_LOCAL_ENV_SITE_ENTRY_PORT, "VCOSMOS_LOCAL_ENV_SITE_ENTRY_PORT is none, please check env var"

    logging.debug(f"{HOST_IP=}")
    logging.debug(f"{VCOSMOS_LOCAL_ENV_SITE_ENTRY_PORT=}")
    atc_url = f"https://{HOST_IP}:{VCOSMOS_LOCAL_ENV_SITE_ENTRY_PORT}"
    return atc_url


def gen_hp_access_authorization() -> str:
    HP_IDP_SERVICE_ID = os.environ.get("HP_IDP_SERVICE_ID")
    HP_IDP_SERVICE_SECRET = os.environ.get("HP_IDP_SERVICE_SECRET")
    assert HP_IDP_SERVICE_ID, "HP_IDP_SERVICE_ID is none, please check env var"
    assert HP_IDP_SERVICE_SECRET, "HP_IDP_SERVICE_SECRET is none, please check env var"

    logging.debug(f"{HP_IDP_SERVICE_ID=}")
    return f"Basic {base64.b64encode(f'{HP_IDP_SERVICE_ID}:{HP_IDP_SERVICE_SECRET}'.encode('ascii')).decode('ascii')}"


def get_hp_access_token() -> dict:
    headers = {
        "Authorization": gen_hp_access_authorization(),
        "Accept": "application/json;charset=utf-8",
        "Content-Type": "application/json;charset=utf-8",
    }
    oauth2_url = "https://login-itg.external.hp.com/as/token.oauth2?grant_type=client_credentials"
    response = httpx.post(oauth2_url, headers=headers, timeout=60, verify=False)
    if response.status_code != 200:
        raise ConnectionError(f"get_hp_access_token failed, status_code: {response.status_code} response: {response.text}")
    hp_access_token = response.json()
    logging.debug(hp_access_token)
    return hp_access_token


def get_vcosmos_token() -> str:
    hp_access_token = get_hp_access_token()
    url = f"{get_atc_url()}/api/auth/login"
    headers = {
        "Accept": "application/json;charset=utf-8",
        "Content-Type": "application/json;charset=utf-8",
        "Authorization": f"{hp_access_token['token_type']} {hp_access_token['access_token']}",
    }
    response = httpx.post(
        url, proxies={}, headers=headers, json={"access_token": hp_access_token["access_token"]}, timeout=60, verify=False
    )
    if response.status_code != 200:
        raise ConnectionError(f"get_vcosmos_token failed, status_code: {response.status_code} response: {response.text}")
    vcosmos_token = response.json().get("token")
    return vcosmos_token


def trigger_plan(vcosmos_token, plan_id) -> dict:
    assert vcosmos_token, "vcosmos_token is none, please check env var"
    assert plan_id, "plan_id is none, please check env var"

    url = f"{get_atc_url()}/api/v2/jobsByPlan?planId={plan_id}"
    headers = {
        "accept": "application/json",
        "content-type": "application/json;charset=utf-8",
        "Authorization": vcosmos_token,
    }
    response = httpx.post(url, proxies={}, verify=False, timeout=60, headers=headers)
    if response.status_code != 200:
        raise ConnectionError(f"trigger_plan failed, status_code: {response.status_code} response: {response.text}")
    return response.json()


def test_trigger_smoking_in_dev_site():
    logging.debug("######################### trigger smoking #########################")
    if os.environ.get("ENV") != "dev":
        return "not dev site, skip"

    if not (SMOKING_TEST_PLAN_ID := os.environ.get("SMOKING_TEST_PLAN_ID")):
        return "no plan id, skip"

    resp = trigger_plan(vcosmos_token=get_vcosmos_token(), plan_id=SMOKING_TEST_PLAN_ID)
    logging.debug(resp)
    logging.debug(f"######################### Job ID {resp.get('jobId')} #########################")
