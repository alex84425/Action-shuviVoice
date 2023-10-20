import json
import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


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
    COMMON_SHUTTLE: Path = Path("/vCosmos_Shuttle", "common", "action")
    ASSETS_FILE_BACKUP: Path = COMMON_SHUTTLE / PROJECT_NAME / "example" / "v0.1.0"
    ASSETS_FILE_LATEST: Path = COMMON_SHUTTLE / PROJECT_NAME / "example" / "v0.2.0"


async def is_assets_exists(assets_key: Path):
    if not isinstance(assets_key, Path):
        raise TypeError("assets_key must be a Path object")
    unready_files = assets_key.rglob("*.part.minio")
    return assets_key.exists() and not list(unready_files)


@lru_cache
def get_settings() -> Settings:
    return Settings()
