# -*- coding: utf-8 -*-
import os
from collections import OrderedDict
from functools import lru_cache
from json import JSONDecoder
from pathlib import Path

import vcosmosapiclient
from pydantic import BaseSettings


def get_history(history_path: Path = Path(__file__).with_name("history.json")):
    history_json_raw = history_path.read_text()
    history_ordered_dict = JSONDecoder(object_pairs_hook=OrderedDict).decode(history_json_raw)
    return history_ordered_dict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Action-ExecutorTemplate"
    PREFIX: str = os.environ.get("ROOT_PATH", f"/{PROJECT_NAME.lower()}")
    HISTORY: OrderedDict = get_history()
    VERSION: str = list(HISTORY.keys())[0]
    HOME: Path = Path("/data")
    LOG_HOME: Path = HOME / "log"
    SOURCE_VERSION: str = os.environ.get("SOURCE_VERSION", "local")

    DESCRIPTION = f"""
        service: {PROJECT_NAME}
        version: {VERSION}
        history: {list(HISTORY.values())[0]}
        commit id: {SOURCE_VERSION}
        lib version: {vcosmosapiclient.VERSION}
        lib history: {list(vcosmosapiclient.HISTORY.values())[0]}
        """


@lru_cache()
def get_settings() -> Settings:
    return Settings()


@lru_cache()
def get_fake_settings() -> Settings:
    return Settings(
        HOME=Path("tests/dummy_home"),
        LOG_HOME=Path("tests/dummy_home") / "log",
        SOURCE_VERSION="4af8f9bef4d13eba48bd51594e244adebfa55ec8",
    )
