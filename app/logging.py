from typing import Dict
import logging
import logging.config

from app import APP_NAME

logger: logging.Logger = logging.getLogger(APP_NAME)


def initialize_logger(logging_config: Dict):
    global logger
    logging.config.dictConfig(logging_config)
    logger.info("Logger initialized")
