# -*- coding: utf-8 -*-
import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Action-HelloWorld"
    PREFIX: str = os.environ.get("ROOT_PATH", f"/{PROJECT_NAME.lower()}")
    VERSION: str = "0.0.1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    HOME: Path = Path("/data")


class FakeSettings(Settings):
    HOME: Path = Path("tests/dummy_home")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_fake_settings() -> Settings:
    return FakeSettings()