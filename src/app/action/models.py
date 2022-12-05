from pydantic import BaseModel, Field
from vcosmosapiclient.models import BaseActionModel


class MyDataModel(BaseModel):
    text_bar: str = Field("", alias="Text Bar")
    text_box: str = Field("numbers 0-9 is not allow in this text box", maxLength=30000, alias="Text Box")

    class Config:
        allow_population_by_field_name = True


class MyActionDataModel(BaseModel):
    data: MyDataModel


class MyActionPostModel(BaseActionModel):
    actionData: MyActionDataModel


class ErrorMonitorModel(BaseModel):
    workingDirectory: str


class DebugModel(BaseModel):
    cmd: str
