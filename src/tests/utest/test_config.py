# -*- coding: utf-8 -*-
from collections import OrderedDict

from app.config import get_history, get_settings
from packaging import version
from pydantic import BaseSettings


def test_get_history():
    """version should match the semantics format."""
    history = get_history()
    assert isinstance(history, OrderedDict)
    for key in history.keys():
        assert isinstance(version.parse(key), version.Version)


def test_get_settings():
    assert isinstance(get_settings(), BaseSettings)
