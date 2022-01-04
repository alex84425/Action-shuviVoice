# -*- coding: utf-8 -*-
from app.config import get_settings
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root():
    return {"service": get_settings().PROJECT_NAME, "version": get_settings().VERSION}


@router.get("/ping")
async def pong():
    return {"ping": "pong!"}
