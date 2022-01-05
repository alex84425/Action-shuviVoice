# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel
from vcosmosapiclient.models import BaseActionModel


class MyDataModel(BaseModel):
    pass


class MyActionDataModel(BaseModel):
    type: str
    version: str
    data: MyDataModel
    index: Optional[int] = 0
    haltOnError: Optional[bool] = False


class MyActionPostModel(BaseActionModel):
    actionData: MyActionDataModel