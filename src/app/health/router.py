# -*- coding: utf-8 -*-
from app.config import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}


@router.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"service": settings.PROJECT_NAME, "Version": settings.VERSION}


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/version")
async def version(settings: Settings = Depends(get_settings)):
    return {"ENVIRONMENT": settings.ENVIRONMENT}
