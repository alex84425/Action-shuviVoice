# -*- coding: utf-8 -*-
import os
from functools import lru_cache

from app.log import actionlogger
from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "ActionInfo-WinPVT"

    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    AF_URL: str = os.getenv(
        "AF_URL", "https://vcosmos.hpcloud.hp.com/api/v1/AF"
    )


@lru_cache()
def get_settings() -> BaseSettings:
    actionlogger.info("Loading config settings from the environment...")
    return Settings()
