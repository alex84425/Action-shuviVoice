import pytest
from vcosmosapiclient.models import TargetModel


@pytest.mark.parametrize(
    "input, expected",
    [
        ({"ip": "192.168.1.111", "port": "43001", "protocol": "https"}, "https://192.168.1.111:43001/file"),
        ({"ip": "192.168.1.111", "port": "8080", "protocol": "http"}, "http://192.168.1.111:8080/file"),
    ],
)
def test_target_model(input, expected):
    obj = TargetModel.parse_obj(input)
    protocol = obj.protocol
    ip = obj.ip
    port = obj.port
    assert expected == f"{protocol}://{ip}:{port}/file"
