import datetime
import logging
import os

import pytest
from feature_test.helper import BVT_TEST_CASES, INTEGRATION_TEST_CASES
from vcosmosapiclient.integration.atc_api_helper import ATC, ATC_SINGLETON
from vcosmosapiclient.integration.azure_test_plan_helper import AzureTestPlanHelper
from vcosmosapiclient.integration.feature_test_helper import (
    UUT_GROUPS,
    polling_result_from_atc_and_update_github_and_azure,
    run_test_on_atc_and_update_github_commits_status,
    subscribe_task_done_or_exception_and_callback_to_github_checker,
)
from vcosmosapiclient.integration.feature_test_models import FeatureTestCase
from vcosmosapiclient.integration.github_helper import GitHubHelper

logging.getLogger().setLevel(logging.DEBUG)
ACTION_NAME = os.environ.get("actionNameLow")  # action-xxx
TASK_TIMEOUT: int = int(datetime.timedelta(minutes=3).total_seconds())


# load env variables
try:
    # github helper
    repository_name = os.environ["RepositoryName"]
    source_version = os.environ["SourceVersion"]
    pat = os.environ["GITHUB_STATUS"]

    # ado helper
    azure_pat = os.environ["AZ_PAT_TEST_PLANS"]
except KeyError as error:
    raise KeyError(f"Missing env for test, (reason {error})") from error

# init atc helper
atc_helper: ATC = ATC_SINGLETON

# init github helper
github_helper: GitHubHelper = GitHubHelper(
    base_url="https://github.azc.ext.hp.com", repository_name=repository_name, source_version=source_version, pat=pat
)

# init azure helper
azure_helper: AzureTestPlanHelper = AzureTestPlanHelper(base_url="https://dev.azure.com/hp-csrd-validation/vCosmos", pat=azure_pat)


async def update_uut_group_id_by_stage_in_place(stage, payload):
    mapping_key = payload["instanceSets"][0]["uutGroup"]["uutGroupId"]
    payload["instanceSets"][0]["uutGroup"]["uutGroupId"] = UUT_GROUPS[mapping_key][stage]


@pytest.mark.asyncio
@pytest.mark.parametrize("action_name", [ACTION_NAME])
async def test_testdev_integration_test(action_name):
    # Testing on few stage and test type first
    assert action_name, "action_name is none, please set it"
    stage = os.environ["ENV"]
    test_type = os.environ.get("DEPLOYMENT_TEST_TYPE")

    # FIXME: not able to get this env variable
    # https://github.azc.ext.hp.com/BPSValidation/AzureReleasePipelines-Test/blob/master/releaseTestExecuteEach.sh#L28
    logging.debug(f"{stage=} {test_type=}")
    if stage == "dev":  # and test_type == "BVT":
        logging.info("Start to trigger BVT test")
        test_cases: list[FeatureTestCase] = BVT_TEST_CASES
    elif stage == "qa":  # and test_type == "INTEGRATION":
        logging.info("Start to trigger INTEGRATION test")
        test_cases: list[FeatureTestCase] = INTEGRATION_TEST_CASES
    else:
        return "Skip test."

    # get vcosmos token, let atc helper ready to use
    await atc_helper.init()

    # 1. run test on ATC, and update github commits status
    for test_case in test_cases:
        await update_uut_group_id_by_stage_in_place(stage, test_case.payload)

    await run_test_on_atc_and_update_github_commits_status(test_cases=test_cases, atc=atc_helper, github=github_helper)

    # 2a. polling result from ATC concurrently
    # FIXME TEST IN DEV, need to move to QA
    if stage == "dev":
        await polling_result_from_atc_and_update_github_and_azure(
            test_cases=test_cases, atc=atc_helper, github=github_helper, azure=azure_helper, timeout=TASK_TIMEOUT
        )

    # 2b. subscribe result from ATC in parallel
    if stage == "NOT_READY":
        await subscribe_task_done_or_exception_and_callback_to_github_checker(test_cases=test_cases, atc=atc_helper, github=github_helper)
