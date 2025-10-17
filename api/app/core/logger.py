# -*- coding: utf-8 -*-
"""
Created on 2025/10/16 21:37

@author: Aidan
@project: GoalBet
@filename: logger
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from api.app.core.settings import settings

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOG_DIR = Path(__file__).parent.parent.parent / 'log'
LOG_DIR.mkdir(exist_ok=True)


def setup_logger(name: str = 'goalbet') -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    if getattr(settings, "log2file", False):
        file_handler = RotatingFileHandler(
            LOG_DIR / "goalbet.log", maxBytes=1024 * 1024 * 10, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    logger.info("Logger setup completed")

    return logger


logger = setup_logger()


def get_logger():
    return logger
