# -*- coding: utf-8 -*-
import os

from app.config import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/")
async def root(config: Settings = Depends(get_settings)):
    return {
        "service": config.PROJECT_NAME,
        "version": config.VERSION,
    }


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}


@router.get("/data")
def show_data(config: Settings = Depends(get_settings)):
    """run in an external threadpool"""

    def path_to_dict(path):
        d = {"name": os.path.basename(path)}
        if os.path.isdir(path):
            d["type"] = "directory"
            d["children"] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
        else:
            d["type"] = "file"
        return d

    return path_to_dict(str(config.HOME))
