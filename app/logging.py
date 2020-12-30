from typing import Dict
from logging import Logger, getLogger
from logging.config import dictConfig

from app import APP_NAME

logger: Logger = getLogger(APP_NAME)


def initialize_logger(logging_config: Dict):
    global logger
    dictConfig(logging_config)
    logger.info("Logger initialized")
