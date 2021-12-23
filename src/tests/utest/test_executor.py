# -*- coding: utf-8 -*-
# FIXME some code is no longer necessary in this action
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


# @pytest.fixture
# def presignurl_payload():
#     filename = Path(dir_path, "presignurl.json")
#     with open(filename) as json_file:
#         obj = json.load(json_file)
#         return obj


# @pytest.fixture
# def presignurl_live():
#     af_url = "https://vcosmos.hpcloud.hp.com/api/v1/AF"
#     guid = "2a86dc11-66f4-4ccb-87d3-74cf4d348531"
#     version = "1.0.0"
#     base_url = "{AF_URL}/testCase/guid/{guid}/{version}/presignedDownloadUrl"
#     url = base_url.format(AF_URL=af_url, guid=guid, version=version)

#     response = requests.get(url=url)
#     response_data = response.json()
#     return response_data


# @pytest.fixture
# def testcase():
#     obj = {"guid": "2a86dc11-66f4-4ccb-87d3-74cf4d348531", "version": "1.0.0", "name": "VCS_VCT_PingUUT"}
#     return obj


# @pytest.fixture
# def s3_path():
#     obj = {"s3Path": "5bd807e9b3144152d8913d23e04e364bdb56cd46aa7cc8a95b159c2b9f6eb1f1"}
#     return obj


# # TODO: mock
# @pytest.mark.asyncio
# async def test_get_path_from_af(testcase, presignurl_payload, monkeypatch):
#     expect_result = "5bd807e9b3144152d8913d23e04e364bdb56cd46aa7cc8a95b159c2b9f6eb1f1"
#     expect_testname = "VCS_VCT_PingUUT"

#     async def mock_get_path_from_af(guid, version):
#         return (
#             presignurl_payload["presignedDownloadUrl"],
#             200,
#             testcase["name"],
#         )

#     monkeypatch.setattr(executor, "get_path_from_af", mock_get_path_from_af)

#     response_data, response_status, response_name = await executor.get_path_from_af(
#         guid=testcase["guid"], version=testcase["version"],
#     )

#     assert response_status == 200
#     assert response_name == expect_testname
#     assert expect_result in response_data


# @pytest.mark.asyncio
# async def test_get_s3_presignurl(testcase, presignurl_payload, monkeypatch):
#     expect_result = "5bd807e9b3144152d8913d23e04e364bdb56cd46aa7cc8a95b159c2b9f6eb1f1"

#     async def mock_get_s3_presignurl(guid, version):
#         return presignurl_payload["presignedDownloadUrl"], 200

#     monkeypatch.setattr(executor, "get_s3_presignurl", mock_get_s3_presignurl)

#     response_data, response_status = await executor.get_s3_presignurl(
#         guid=testcase["guid"], version=testcase["version"],
#     )

#     assert response_status == 200
#     assert expect_result in response_data


# def test_presignurl_filename(presignurl_payload: dict, monkeypatch):
#     presigned_url = presignurl_payload["presignedDownloadUrl"]

#     estimated_name = "5bd807e9b3144152d8913d23e04e364bdb56cd46aa7cc8a95b159c2b9f6eb1f1.zip"
#     filename = executor.presignurl_filename(presigned_url)

#     assert filename == estimated_name


# # mock the return zip file name
# @pytest.mark.asyncio
# async def test_get_testcase_file_from_af(presignurl_live: dict, monkeypatch):
#     filename = "cdb5fc971969e2d6ecd9fe684360496049cb52f7f14a5e720bf122985b1dacc7.zip"
#     filedir = os.getcwd()
#     presignedDownloadUrl = presignurl_live["presignedDownloadUrl"]

#     estimated_filename = filename
#     estimated_filepath = Path(filedir, filename)

#     async def mock_get_file_from_af(presignedDownloadUrl, filedir):
#         return filename, Path(filedir, filename)

#     monkeypatch.setattr(executor, "get_file_from_af", mock_get_file_from_af)

#     actual_filename, actual_filepath = await executor.get_file_from_af(presignedDownloadUrl=presignedDownloadUrl, filedir=filedir)

#     assert estimated_filename == actual_filename
#     assert estimated_filepath == actual_filepath


# @pytest.mark.asyncio
# async def test_get_testcase_file_from_af_not_exist():
#     filename = "test123"
#     result = await executor.check_cache(filename=filename, filedir=os.getcwd())

#     assert result is False


# @pytest.mark.asyncio
# async def test_get_testcase_file_from_af_exist():
#     file = open("testcase_file_exist.txt", "w+")
#     file.write("test context \n")
#     file.close()
#     result = await executor.check_cache(filename=file.name, filedir=os.getcwd())

#     assert result

#     os.remove(file.name)


# @pytest.mark.asyncio
# async def test_get_testcase_file_from_af_with_0_size():
#     file = open("testcase_file_with_0_size.txt", "w+")
#     file.close()
#     result = await executor.check_cache(filename=file.name, filedir=os.getcwd())

#     assert result is False


# @pytest.mark.asyncio
# async def test_get_testcase_path_from_cache():
#     filename = "cdb5fc971969e2d6ecd9fe684360496049cb52f7f14a5e720bf122985b1dacc7.zip"
#     filedir = os.getcwd()

#     estimated_filepath = Path(filedir, filename)
#     actual_filename, actual_filepath = await executor.get_testcase_path_from_cache(filename, filedir)

#     assert actual_filename == filename
#     assert actual_filepath == estimated_filepath


# @pytest.mark.asyncio
# async def test_get_s3_presignurl_form_provider(s3_path, monkeypatch, presignurl_payload):

#     expect_result = "5bd807e9b3144152d8913d23e04e364bdb56cd46aa7cc8a95b159c2b9f6eb1f1"

#     async def mock_get_s3_presignurl_form_provider(s3_path):
#         return presignurl_payload["presignedDownloadUrl"], 200

#     monkeypatch.setattr(executor, "get_s3_presignurl_form_provider", mock_get_s3_presignurl_form_provider)

#     response_data, response_status = await executor.get_s3_presignurl_form_provider(
#         s3_path=s3_path
#     )

#     assert response_status == 200
#     assert expect_result in response_data
