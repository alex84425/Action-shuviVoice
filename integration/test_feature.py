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
OVERALL_TASK_TIMEOUT: int = int(datetime.timedelta(minutes=10).total_seconds())


async def update_uut_group_id_by_stage_in_place(stage, payload):
    mapping_key = payload["instanceSets"][0]["uutGroup"]["uutGroupId"]
    payload["instanceSets"][0]["uutGroup"]["uutGroupId"] = UUT_GROUPS[mapping_key][stage]


@pytest.mark.asyncio
@pytest.mark.parametrize("action_name", [ACTION_NAME])
async def test_testdev_integration_test(action_name):
    # Testing on few stage and test type first
    assert action_name, "action_name is none, please set it"
    site = os.environ["SITE"]
    logging.debug(f"{site=}")

    stage = os.environ["ENV"]
    logging.debug(f"{stage=}")

    test_type = os.environ.get("DEPLOYMENT_TEST_TYPE")
    logging.debug(f"{test_type=}")

    release_environment_name = os.environ.get("RELEASE_ENVIRONMENTNAME")
    logging.debug(f"{release_environment_name=}")

    # github helper
    repository_name = os.environ.get("RepositoryName")
    source_version = os.environ.get("SourceVersion")
    github_pat = os.environ.get("GITHUB_STATUS")

    # ado helper
    azure_pat = os.environ.get("AZ_PAT_TEST_PLANS")
    if stage == "dev" and site == "hp-tnn-dev" and test_type == "BVT":
        logging.info("Start to trigger BVT test")
        test_cases: list[FeatureTestCase] = BVT_TEST_CASES
        # if azure helper is None, it will not update azure test point
        azure_helper = None
    elif (
        stage == "qa" and site == "hp-tnn-qa" and release_environment_name == "Proxy Testing on QA"
    ):  # move INTEGRATION_TEST_CASES to ITG 'End to End' when the stage ready.
        logging.info("Start to trigger INTEGRATION test")
        test_cases: list[FeatureTestCase] = INTEGRATION_TEST_CASES
        # init azure helper
        azure_helper = AzureTestPlanHelper(base_url="https://dev.azure.com/hp-csrd-validation/vCosmos", pat=azure_pat)
    else:
        return "Skip test."

    # init atc helper, get vcosmos token
    atc_helper: ATC = ATC_SINGLETON
    await atc_helper.init()

    # init github helper
    github_helper: GitHubHelper = GitHubHelper(
        base_url="https://github.azc.ext.hp.com",
        repository_name=repository_name,
        source_version=source_version,
        pat=github_pat,
    )

    # 1. run test on ATC, and update github commits status
    for test_case in test_cases:
        await update_uut_group_id_by_stage_in_place(stage, test_case.payload)

    await run_test_on_atc_and_update_github_commits_status(test_cases=test_cases, atc=atc_helper, github=github_helper)

    # 2a. polling result from ATC concurrently
    if stage == "qa":
        await polling_result_from_atc_and_update_github_and_azure(
            test_cases=test_cases, atc=atc_helper, github=github_helper, azure=azure_helper, timeout=OVERALL_TASK_TIMEOUT
        )

    # 2b. subscribe result from ATC in parallel
    if stage == "dev":
        await subscribe_task_done_or_exception_and_callback_to_github_checker(test_cases=test_cases, atc=atc_helper, github=github_helper)
