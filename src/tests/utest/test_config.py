from packaging import version
from pydantic import BaseSettings

from app.config import get_history, get_settings


def test_get_history():
    """version should match the semantics format."""
    history = get_history(get_settings().PROJECT_NAME)
    assert isinstance(history, dict)
    for key in history:
        assert isinstance(version.parse(key), version.Version)


def test_get_settings():
    assert isinstance(get_settings(), BaseSettings)
