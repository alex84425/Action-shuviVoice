# -*- coding: utf-8 -*-
"""
This module contains some mandatory endpoints

Required endpoint
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/tree/master/ActionExecutor#required-endpoint--contract

Response schema:
https://github.azc.ext.hp.com/BPSVCommonService/Action-Development-Guideline/blob/master/ActionExecutor/ActionActResponse.schema.json
"""

from app.action import models
from app.action.executor import execute
from app.config import Settings, get_fake_settings, get_settings
from fastapi import APIRouter, Depends
from vcosmosapiclient.depends import ApiDepends, FakeDepends
from vcosmosapiclient.utils import validator

router = APIRouter()


@router.get("/info")
async def info(config: Settings = Depends(get_settings)):
    return {"type": config.PROJECT_NAME, "typeVer": config.VERSION, "sourceVer": config.SOURCE_VERSION}


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.post("/dryrun")
@validator.post
async def post_to_action_dryrun(act: models.MyActionPostModel, api: FakeDepends = Depends(), config: Settings = Depends(get_fake_settings)):
    # this endpoint may deprecated
    return await post_to_action(act, api, config)


@router.post("/act")
@validator.post
async def post_to_action(act: models.MyActionPostModel, api: ApiDepends = Depends(), config: Settings = Depends(get_settings)):
    return await execute(act)
