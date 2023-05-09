import logging
from pathlib import Path

from vcosmosapiclient.integration.atc_api_helper import ATC_SINGLETON
from vcosmosapiclient.integration.feature_test_models import FeatureTestCase, ResultNotMatchError, StatusNotMatchError, Task


async def hello_world_example_should_pass_checker(task: Task):
    logging.debug("hello_world_example_should_pass_checker")

    if await task.get_status() != "PASS":
        raise StatusNotMatchError
    logging.debug("actual_status as expected")

    expected_result = {"Text Bar": "Hello", "Text Box": "World"}
    actual_result = await task.get_result()
    if expected_result != actual_result:
        raise ResultNotMatchError
    logging.debug("actual_result as expected even we test very details")

    expected_content = "Hello"
    async with task.get_stored_files(atc=ATC_SINGLETON) as temp_log_path:
        for file in temp_log_path.glob("**/*hello.txt"):
            content = file.read_text().strip()
            if content != expected_content:
                raise ResultNotMatchError("The file content is not as expected")
            break
        else:
            raise ResultNotMatchError("Can't find the file we want to check")
    logging.debug("stored files is as expected!")


HERE = Path(__file__).parent
BVT_TEST_CASES = [
    FeatureTestCase(
        payload_path=HERE / "hello_world_example_should_pass.json",
        checker=hello_world_example_should_pass_checker,
    )
]
INTEGRATION_TEST_CASES = [
    FeatureTestCase(
        payload_path=HERE / "hello_world_example_should_pass.json",
        checker=hello_world_example_should_pass_checker,
    )
]