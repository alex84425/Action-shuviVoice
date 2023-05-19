# this is a cli tool, which can be used to check the correctness of the feature test
import argparse
import asyncio
import json
import logging
import os

from feature_test.helper import BVT_TEST_CASES
from vcosmosapiclient.integration.atc_api_helper import ATC, ATC_SINGLETON
from vcosmosapiclient.integration.feature_test_helper import task_status_checker
from vcosmosapiclient.integration.feature_test_models import FeatureTestCase
from vcosmosapiclient.integration.github_helper import GitHubHelper

logging.getLogger().setLevel(logging.DEBUG)


async def main():
    test_cases: list[FeatureTestCase] = BVT_TEST_CASES

    # Fail if some env is not set
    logging.info("Prepare ENV variables:")
    github_pat = os.environ["STATUS_GITHUB"]
    github_ref = os.environ["GITHUB_REF"].split("heads/")[-1]

    get dispatch_parameters
    parser = argparse.ArgumentParser(description="Feature Test Checker")
    parser.add_argument("dispatch_parameters", type=str, help="ATC task done subscription callback dispatch_parameters")

    args = parser.parse_args()
    valid_json_data = args.dispatch_parameters.replace("'", '"')
    dispatch_parameters = json.loads(valid_json_data)
    logging.info(f"{dispatch_parameters=}")
    source_version = dispatch_parameters["source_version"]
    repository_name = dispatch_parameters["repository_name"]

    # init atc helper, get vcosmos token
    atc_helper: ATC = ATC_SINGLETON
    await atc_helper.init()

    # init github helper
    github_helper: GitHubHelper = GitHubHelper(
        base_url="https://github.azc.ext.hp.com",
        repository_name=repository_name,
        source_version=source_version,
        pat=github_pat,
        # FIXME USE THIS FOR TESTING
        branch_name=github_ref,
    )

    # check task status
    await task_status_checker(dispatch_parameters, test_cases, atc_helper, github_helper)


if __name__ == "__main__":
    asyncio.run(main())
