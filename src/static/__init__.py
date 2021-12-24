from pathlib import Path

THIS = Path(__file__)


def file(filename) -> Path:
    return THIS.with_name(filename)
