# -*- coding: utf-8 -*-
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
