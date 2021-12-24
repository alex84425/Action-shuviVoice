# -*- coding: utf-8 -*-
import logging


def set_log_config(
    fmt="{asctime} {levelname:.1s} - {message} <{filename} ({lineno})>",
    level=logging.DEBUG,
):
    formatter = logging.Formatter(fmt, style="{")

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger("action-smr")
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger


atclogger = set_log_config()
