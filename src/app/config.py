import json
import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings


def get_history(project_name: str) -> dict:
    history_folder = Path(__file__).parent
    history_path = history_folder / f"{project_name.lower()}-history.json"
    if not history_path.exists():
        # fallback to history.json if {project_name}-history.json file not exists
        history_path = history_folder / "history.json"
    return json.loads(history_path.read_text())


class Settings(BaseSettings):
    # local run loads environment variables from load.env; online run loads real environment variables
    PROJECT_NAME: str = os.environ.get("ACTION_TYPE", "Action-Dummy")
    PATH_PREFIX: str = "/"
    HISTORY: dict = get_history(PROJECT_NAME)
    VERSION: str = next(iter(HISTORY.keys()))
    VOLUME: Path = Path(os.environ.get("VOLUME_MOUNT_PATH", "/data"))
    LOG_FOLDER: Path = VOLUME / "log"
    SOURCE_VERSION: str = "local"
    HOSTNAME_AND_PORT: str = f"{PROJECT_NAME.lower()}:{os.environ.get('PORT')}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
