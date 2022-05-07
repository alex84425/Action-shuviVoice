# -*- coding: utf-8 -*-
import collections
import json
import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings

history = Path(__file__).with_name("history.json")
with open(history) as f:
    HISTORY = f.read()
    HISTORY = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(HISTORY)
    LAST_VERSION = list(HISTORY.keys())[0]


class Settings(BaseSettings):
    PROJECT_NAME: str = "Action-ExecutorTemplate"
    PREFIX: str = os.environ.get("ROOT_PATH", f"/{PROJECT_NAME.lower()}")
    VERSION: str = LAST_VERSION
    HISTORY: dict = HISTORY
    SOURCE_VERSION: str = os.environ.get("SOURCE_VERSION", "unknown")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "dev")
    HOME: Path = Path("/data")
    LOG_HOME: Path = HOME / "log"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_fake_settings() -> Settings:
    return Settings(
        HOME=Path("tests/dummy_home"),
        LOG_HOME=Path("tests/dummy_home") / "log",
    )
