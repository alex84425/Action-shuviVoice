import asyncio
import json
import logging
import os
import sys
from pathlib import Path

from loguru import logger

BASE_DIR = os.path.dirname(os.path.dirname((os.path.dirname((os.path.abspath(__file__))))))
LOG_PATH = Path(BASE_DIR, "log")


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: "CRITICAL",
        40: "ERROR",
        30: "WARNING",
        20: "INFO",
        10: "DEBUG",
        0: "NOTSET",
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1
        try:
            task_id = asyncio.current_task().get_name()
        except Exception:
            task_id = "NoTask"
        log = logger.bind(task_id=task_id)
        msgs = record.getMessage()
        if not msgs:
            log.opt(depth=depth, exception=record.exc_info).log(level, msgs)
        else:
            for msg in msgs.splitlines():
                log.opt(depth=depth, exception=record.exc_info).log(level, msg)


def setup_logging(config_path):

    with open(config_path) as config_file:
        config = json.load(config_file)["logger"]

    filepath = Path(config.get("filepath"))
    filepath.parent.mkdir(parents=True, exist_ok=True)
    level = config.get("level")
    retention = config.get("retention")
    rotation = config.get("rotation")
    format = config.get("format")

    logger.remove()
    logger.add(sys.stdout, enqueue=False, backtrace=False, diagnose=False, level=level.upper(), format=format)
    logger.add(
        str(filepath),
        rotation=rotation,
        retention=retention,
        enqueue=False,
        backtrace=False,
        diagnose=False,
        level=level.upper(),
        format=format,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0)
    for _log in ["uvicorn", "uvicorn.error", "fastapi", "uvicorn.access"]:
        _logger = logging.getLogger(_log)
        _logger.handlers = [InterceptHandler()]
