from pathlib import Path

from vcosmosapiclient.integration.atc_api_helper import ATC_SINGLETON
from vcosmosapiclient.integration.feature_test_models import FeatureTestCase, Task


async def hello_world_single_line_example_should_pass_checker(task: Task):
    await task.status_should_be_pass()
    await task.result_should_be({"Operation": "Single Line", "text_bar": "Hello World"})
    async with task.get_stored_files(atc=ATC_SINGLETON) as temp_log_path:
        await task.file_content_should_be(temp_log_path, "hello.txt", expected_content="Hello")


async def hello_world_multi_line_example_should_pass_checker(task: Task):
    await task.status_should_be_pass()
    await task.result_should_be({"Operation": "Multi Line", "text_box": "Hello \nWorld"})
    async with task.get_stored_files(atc=ATC_SINGLETON) as temp_log_path:
        await task.file_content_should_be(temp_log_path, "hello.txt", expected_content="Hello")


async def daemon_mode_operation_1_should_pass(task: Task):
    daemon_action_index = 0
    await task.status_should_be_pass(action_id=daemon_action_index)


async def daemon_mode_operation_2_should_pass(task: Task):
    daemon_action_index = 0
    await task.status_should_be_pass(action_id=daemon_action_index)


HERE = Path(__file__).parent
BVT_TEST_CASES = [
    FeatureTestCase(
        payload_path=HERE / "hello_world_single_line_example_should_pass.json",
        checker=hello_world_single_line_example_should_pass_checker,
    ),
    FeatureTestCase(
        payload_path=HERE / "hello_world_multi_line_example_should_pass.json",
        checker=hello_world_multi_line_example_should_pass_checker,
    ),
    FeatureTestCase(
        payload_path=HERE / "daemon_mode_operation_1_should_pass.json",
        checker=daemon_mode_operation_1_should_pass,
    ),
    FeatureTestCase(
        payload_path=HERE / "daemon_mode_operation_2_should_pass.json",
        checker=daemon_mode_operation_2_should_pass,
    ),
]
INTEGRATION_TEST_CASES = [
    FeatureTestCase(
        payload_path=HERE / "hello_world_single_line_example_should_pass.json",
        checker=hello_world_single_line_example_should_pass_checker,
    ),
    FeatureTestCase(
        payload_path=HERE / "hello_world_multi_line_example_should_pass.json",
        checker=hello_world_multi_line_example_should_pass_checker,
    ),
    FeatureTestCase(
        payload_path=HERE / "daemon_mode_operation_1_should_pass.json",
        checker=daemon_mode_operation_1_should_pass,
    ),
    FeatureTestCase(
        payload_path=HERE / "daemon_mode_operation_2_should_pass.json",
        checker=daemon_mode_operation_2_should_pass,
    ),
]
