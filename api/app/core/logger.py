# -*- coding: utf-8 -*-
"""
Created on 2025/10/16 21:37

@author: Aidan
@project: GoalBet
@filename: logger
"""
import logging
from logging.handlers import RotatingFileHandler

LOG_FORMAT = "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str = 'goalbet', log2file: bool = False) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    if log2file:
        file_handler = RotatingFileHandler(
            '../log/goalbet.log', maxBytes=1024 * 1024 * 10, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger
