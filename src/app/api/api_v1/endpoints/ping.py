# -*- coding: utf-8 -*-
from pathlib import Path

from app.core.config import Settings, get_settings
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/ping")
async def pong():
    """https://15.36.156.53/actioninfo-winpvt/api/v1/ping"""
    return {"ping": "pong!"}


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/version")
async def version(settings: Settings = Depends(get_settings)):
    return {
        "ENVIRONMENT": settings.ENVIRONMENT,
        "AF_URL": settings.AF_URL,
    }


@router.get("/test")
async def test():
    return {"test": Path("/app/test.txt").read_text()}
