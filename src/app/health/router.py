# -*- coding: utf-8 -*-
import os
import traceback

from ansi2html import Ansi2HTMLConverter
from app.config import Settings, get_settings
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

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


@router.get("/log", response_class=HTMLResponse)
def log(config: Settings = Depends(get_settings)):
    try:
        content = []
        for item in config.LOG_HOME.iterdir():
            if item.is_file():
                content.append(f'<a href="{config.PREFIX}/log/{item.name}">{item.name}</a>')

        return "<br>".join(content)
    except Exception:
        return traceback.format_exc().replace("\n", "<br>")


@router.get("/log/{filename}", response_class=HTMLResponse)
def log_file(filename: str, config: Settings = Depends(get_settings)):
    try:
        with open(config.LOG_HOME / filename, encoding="utf-8") as f:
            data = f.read()

        con = Ansi2HTMLConverter()
        data = con.convert(data)
        return data
    except Exception:
        return traceback.format_exc().replace("\n", "<br>")
