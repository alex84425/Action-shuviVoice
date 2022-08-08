import json
import os
from functools import lru_cache
from pathlib import Path

import vcosmosapiclient
from pydantic import BaseSettings


def get_history(project_name: str) -> dict:
    history_folder = Path(__file__).parent
    history_path = history_folder / f"{project_name.lower()}-history.json"
    if not history_path.exists():
        # fallback to history.json if {project_name}-history.json file not exists
        history_path = history_folder / "history.json"
    return json.loads(history_path.read_text())


class Settings(BaseSettings):
    # local run loads environment virables from load.env; online run loads real environment variables
    PROJECT_NAME: str = "Action-ExecutorTemplate"
    PATH_PREFIX: str = "/"
    HISTORY: dict = get_history(PROJECT_NAME)
    VERSION: str = list(HISTORY.keys())[0]
    VOLUME: Path = Path(os.environ.get("VOLUME_MOUNT_PATH", "/data"))
    LOG_FOLDER: Path = VOLUME / "log"
    SOURCE_VERSION: str = "local"
    HOSTNAME_AND_PORT: str = f"{PROJECT_NAME.lower()}:{os.environ.get('PORT')}"

    DESCRIPTION = f"""
        service: {PROJECT_NAME}
        version: {VERSION}
        history: {list(HISTORY.values())[0]}
        commit id: {SOURCE_VERSION}
        lib version: {vcosmosapiclient.VERSION}
        lib history: {list(vcosmosapiclient.HISTORY.values())[0]}
        """


@lru_cache
def get_settings() -> Settings:
    return Settings()


@lru_cache
def get_fake_settings() -> Settings:
    return Settings(
        VOLUME=Path("tests/dummy_volume"),
        LOG_FOLDER=Path("tests/dummy_volume") / "log",
        SOURCE_VERSION="4af8f9bef4d13eba48bd51594e244adebfa55ec8",
    )
