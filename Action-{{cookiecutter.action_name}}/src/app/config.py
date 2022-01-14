# -*- coding: utf-8 -*-
import os
from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Action-{{cookiecutter.action_name}}"
    PREFIX: str = os.environ.get("ROOT_PATH", f"/{PROJECT_NAME.lower()}")
    VERSION: str = "0.0.1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")


@lru_cache()
def get_settings() -> Settings:
    return Settings()
