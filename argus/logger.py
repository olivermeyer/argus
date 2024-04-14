import json
import logging
import os
import time
from typing import Any

import requests


class Logger(logging.Logger):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args)
        self.loki_url = kwargs.get("loki_url", None)
        self.labels = kwargs.get("labels", {})

    def log_to_loki(self, msg: object, level: str):
        payload = {
            "streams": [
                {
                    "stream": {"application": "argus"},
                    "values": [[str(time.time_ns()), f"[{level}] {msg}"]],
                }
            ]
        }
        headers = {"Content-type": "application/json"}
        payload = json.dumps(payload)
        response = requests.post(self.loki_url, data=payload, headers=headers)
        response.raise_for_status()
        return response

    def info(self, msg: object, *args: Any, **kwargs: Any):
        self.log_to_loki(msg, "INFO")
        super().info(msg, *args, **kwargs)

    def debug(self, msg: object, *args: Any, **kwargs: Any):
        # self.log_to_loki(msg, "DEBUG")
        super().debug(msg, *args, **kwargs)

    def warning(self, msg: object, *args: Any, **kwargs: Any):
        self.log_to_loki(msg, "WARNING")
        super().warning(msg, *args, **kwargs)

    def error(self, msg: object, *args: Any, **kwargs: Any):
        self.log_to_loki(msg, "ERROR")
        super().error(msg, *args, **kwargs)

    def critical(self, msg: object, *args: Any, **kwargs: Any):
        self.log_to_loki(msg, "CRITICAL")
        super().critical(msg, *args, **kwargs)


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger.
    """
    if os.environ.get("ENVIRONMENT") == "pro":
        logger = Logger(__name__, loki_url="http://loki:3100/loki/api/v1/push")
    else:
        logger = logging.Logger(__name__)
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    return logger


logger = get_logger()
