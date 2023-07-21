from enum import Enum
from typing import Union

from pydantic import Field, validator
from vcosmosapiclient.models import BaseActionModel, BaseModel


class OperationEnum(str, Enum):
    SINGLE_LINE = "Single Line"
    MULTI_LINE = "Multi Line"


class OperationModel(BaseModel):
    operation: OperationEnum = OperationEnum.SINGLE_LINE


class SingleLineModel(OperationModel):
    text_bar: str = Field("", alias="Text Bar")


class MultiLineModel(OperationModel):
    text_box: str = Field("numbers 0-9 is not allow in this text box", maxLength=30000, alias="Text Box")


class MyDataModel(OperationModel):
    class Config:
        extra = "allow"


class MyActionDataModel(BaseModel):
    data: Union[MyDataModel, SingleLineModel, MultiLineModel]

    @validator("data")
    def get_model_by_operation(cls, value):  # pylint: disable=E0213
        value_dict = value.dict(by_alias=False)
        if value_dict["operation"] == OperationEnum.SINGLE_LINE:
            return SingleLineModel(**value_dict)

        if value_dict["operation"] == OperationEnum.MULTI_LINE:
            return MultiLineModel(**value_dict)

        raise ValueError("Operation is not supported")


class MyActionPostModel(BaseActionModel):
    actionData: MyActionDataModel


class MyActionCallbackModel(BaseModel):
    act: MyActionPostModel = Field(..., alias="_actionMeta")
    example_extra_data: str = ""


class ErrorMonitorModel(BaseModel):
    workingDirectory: str


class DebugModel(BaseModel):
    cmd: str
