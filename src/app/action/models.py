from enum import Enum
from typing import Union

from pydantic import Field, validator
from vcosmosapiclient.models import BaseActionModel, BaseModel


# model mapper for action info and action model
class BaseProviderInputModel(BaseModel):
    pass


# ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ Sync from Action info ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓


# Enum definitions
class MainOperationEnum(str, Enum):
    SINGLE_LINE = "Single Line"
    MULTI_LINE = "Multi Line"


class DaemonOperationEnum(str, Enum):
    OPERATION_1 = "Operation 1"
    OPERATION_2 = "Operation 2"


class DaemonComboBoxEnum(str, Enum):
    COMBOBOX_VALUE_1 = "Value 1"
    COMBOBOX_VALUE_2 = "Value 2"


# Operation models
class MainOperationModel(BaseProviderInputModel):
    Operation: MainOperationEnum = MainOperationEnum.SINGLE_LINE


class DaemonOperationModel(BaseProviderInputModel):
    Operation: DaemonOperationEnum = DaemonOperationEnum.OPERATION_1


# Main operation models
class SingleLineModel(MainOperationModel):
    text_bar: str = Field("", alias="Text Bar")


class MultiLineModel(MainOperationModel):
    text_box: str = Field("numbers 0-9 is not allow in this text box", maxLength=30000, alias="Text Box")


# Daemon operation models
class DaemonPageOneModel(DaemonOperationModel):
    check_box: bool = Field(
        False,
        alias="I am a check box",
        toolTip="<p>I am tool tip</p>I am tool tip second line",
    )
    combo_box: DaemonComboBoxEnum = Field(DaemonComboBoxEnum.COMBOBOX_VALUE_1, alias="I am a combobox")


class DaemonPageTwoModel(DaemonOperationModel):
    int_value: int = Field(
        2,
        ge=1,
        le=5,
        alias="I am an int",
        toolTip="<p>I am tool tip</p>I am tool tip second line",
    )
    string: str = Field(
        "",
        alias="I am a string",
        placeholder="I am placeholder",
    )
    disabled_string: str = Field(
        "",
        alias="I am a disabled string",
        disabled=True,
    )


# Provider input models
class ProviderInput(BaseProviderInputModel):
    class Config:
        extra = "allow"


# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑ Sync from Action info ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑


# get model by operation
class MyActionDataModel(BaseModel):
    daemonMode: bool
    data: Union[ProviderInput, SingleLineModel, MultiLineModel, DaemonPageOneModel, DaemonPageTwoModel]

    @validator("data")
    def get_model_by_operation(cls, field_value, values):  # pylint: disable=E0213
        value_dict = field_value.dict()
        operation = value_dict.get("Operation")

        if values.get("daemonMode"):
            if operation == DaemonOperationEnum.OPERATION_1:
                return DaemonPageOneModel(**value_dict)

            if operation == DaemonOperationEnum.OPERATION_2:
                return DaemonPageTwoModel(**value_dict)
        else:
            if operation == MainOperationEnum.SINGLE_LINE:
                return SingleLineModel(**value_dict)

            if operation == MainOperationEnum.MULTI_LINE:
                return MultiLineModel(**value_dict)

        raise ValueError("Payload is not support")


class MyActionPostModel(BaseActionModel):
    actionData: MyActionDataModel


class MyActionCallbackModel(BaseModel):
    act: MyActionPostModel = Field(..., alias="_actionMeta")
    example_extra_data: str = ""
