# -*- coding: utf-8 -*-
import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "TemplateName"
    PREFIX: str = f"/action-{PROJECT_NAME.lower()}"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    VERSION: str = "0.0.1"
    CTRL_SCHEMA_VER: str = "0.0.1"


@lru_cache()
def get_settings() -> BaseSettings:
    return Settings()
