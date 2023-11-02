from enum import Enum
from typing import Union

from pydantic import ConfigDict, Field, field_validator
from vcosmosapiclient.models import BaseActionModel, BaseModel


# model mapper for action info and action model
class BaseProviderInputModel(BaseModel):
    pass


#########################
# Sync from Action info #
#########################


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
    text_box: str = Field(
        "numbers 0-9 is not allow in this text box",
        alias="Text Box",
        json_schema_extra={
            "maxLength": 30000,
        },
    )


# Daemon operation models
class DaemonPageOneModel(DaemonOperationModel):
    maximum_execution_time: int = Field(
        1 * 60,
        alias="Maximum Execution Time",
        description="this is a duration picker",
        json_schema_extra={
            "ui": "durationPicker",
            "customizedText": "Min: 1 minutes, Max: 24 hours",
            "showHeading": True,
            "maximum": 60 * 60 * 24,
            "minimum": 1 * 60,
        },
    )
    check_box: bool = Field(
        False,
        alias="I am a check box",
        json_schema_extra={
            "toolTip": "<p>I am tool tip</p>I am tool tip second line",
        },
    )
    combo_box: DaemonComboBoxEnum = Field(DaemonComboBoxEnum.COMBOBOX_VALUE_1, alias="I am a combobox")


class DaemonPageTwoModel(DaemonOperationModel):
    maximum_execution_time: int = Field(
        1 * 60,
        alias="Maximum Execution Time",
        description="this is a duration picker",
        json_schema_extra={
            "ui": "durationPicker",
            "customizedText": "Min: 1 minutes, Max: 24 hours",
            "showHeading": True,
            "maximum": 60 * 60 * 24,
            "minimum": 1 * 60,
        },
    )
    int_value: int = Field(
        2,
        ge=1,
        le=5,
        alias="I am an int",
        json_schema_extra={
            "toolTip": "<p>I am tool tip</p>I am tool tip second line",
        },
    )
    string: str = Field(
        "",
        alias="I am a string",
        json_schema_extra={
            "placeholder": "I am placeholder",
        },
    )
    disabled_string: str = Field(
        "",
        alias="I am a disabled string",
        json_schema_extra={
            "disabled": True,
        },
    )


def determine_model(payload: dict):
    operation = payload.get("Operation")
    if payload.get("daemon"):
        if operation == DaemonOperationEnum.OPERATION_1:
            return DaemonPageOneModel(**payload)

        if operation == DaemonOperationEnum.OPERATION_2:
            return DaemonPageTwoModel(**payload)

        return DaemonPageOneModel(**payload)

    if operation == MainOperationEnum.SINGLE_LINE:
        return SingleLineModel(**payload)

    if operation == MainOperationEnum.MULTI_LINE:
        return MultiLineModel(**payload)

    return SingleLineModel(**payload)


#################
# Action Models #
#################
class ProviderInput(BaseProviderInputModel):
    model_config = ConfigDict(extra="allow")


class MyActionDataModel(BaseModel):
    daemonMode: bool
    data: Union[ProviderInput, SingleLineModel, MultiLineModel, DaemonPageOneModel, DaemonPageTwoModel]

    @field_validator("data")
    def determine_model_by_data(cls, value, values):  # pylint: disable=E0213
        payload = value.dict()

        # if payload didn't set daemon, then use daemonMode as its value
        if payload.get("daemon") is None:
            payload["daemon"] = values.data.get("daemonMode", False)
        return determine_model(payload)


class MyActionPostModel(BaseActionModel):
    actionData: MyActionDataModel


class MyActionCallbackModel(BaseModel):
    act: MyActionPostModel = Field(..., alias="_actionMeta")
    example_extra_data: str = ""
