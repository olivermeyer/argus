import logging
import os
from logging.handlers import RotatingFileHandler


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger.
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    file_handler = RotatingFileHandler(
        filename=os.path.join(os.environ["LOG_DIRECTORY"], "argus.log"),
        maxBytes=10*1024*1024,
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


logger = get_logger()
