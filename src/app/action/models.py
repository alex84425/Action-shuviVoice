from pydantic import BaseModel
from vcosmosapiclient.models import BaseActionModel


class MyDataModel(BaseModel):
    MyTestData: str


class MyActionDataModel(BaseModel):
    data: MyDataModel


class MyActionPostModel(BaseActionModel):
    actionData: MyActionDataModel


class ErrorMonitorModel(BaseModel):
    workingDirectory: str


class DebugModel(BaseModel):
    cmd: str
