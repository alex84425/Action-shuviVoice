# -*- coding: utf-8 -*-
import asyncio
import shutil
from pathlib import Path

from app.action import models, scenario
from app.config import Settings, get_settings
from app.log import atclogger as logger
from fastapi import APIRouter, Depends
from fastapi.datastructures import UploadFile
from fastapi.param_functions import File
from vcosmosapiclient.models import ResponseControllerModel

router = APIRouter()


ACTION_NAME = Settings().PROJECT_NAME
ACTION_VERSION = Settings().VERSION
HOME = Path("/data")
SMC_BIN = (HOME / "SMC.zip").resolve()


@router.get("/info")
async def rounter_action_info(settings: Settings = Depends(get_settings)):
    return {"type": settings.PROJECT_NAME, "typeVer": settings.VERSION}


@router.post("/dryrun", response_model=ResponseControllerModel)
async def post_to_action_dryrun(
    request: models.MyActionPostModel,
):

    return await scenario.post_to_action_remote(postact=request, dryrun=True)


@router.post("/act", response_model=ResponseControllerModel)
async def post_to_action(
    request: models.MyActionPostModel,
):
    logger.info(f"request_model = {request.json()}")
    return await scenario.post_to_action_remote(postact=request)


@router.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    def wrapper():
        HOME.mkdir(exist_ok=True)
        with open(SMC_BIN, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)

    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, wrapper)
