import json
import logging
import os
import time
import traceback

import requests


class Logger(logging.Logger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.loki_url = kwargs.get("loki_url", None)

    def log_to_loki(self, msg, level: str, extra: dict | None = None):
        labels = {
            "application": "argus",
        }
        labels = {**labels, **extra} if extra else labels
        payload = {
            "streams": [
                {
                    "stream": labels,
                    "values": [[str(time.time_ns()), f"[{level}] {msg}"]],
                }
            ]
        }
        headers = {"Content-type": "application/json"}
        payload = json.dumps(payload)
        response = requests.post(self.loki_url, data=payload, headers=headers)
        response.raise_for_status()
        return response

    def info(self, msg, *args, extra: dict | None = None, **kwargs):
        self.log_to_loki(msg, "INFO", extra=extra)
        super().info(msg, *args, **kwargs)

    def debug(self, msg, *args, extra: dict | None = None, **kwargs):
        # self.log_to_loki(msg, "DEBUG")
        super().debug(msg, *args, **kwargs)

    def warning(self, msg, *args, extra: dict | None = None, **kwargs):
        self.log_to_loki(msg, "WARNING")
        super().warning(msg, *args, **kwargs)

    def error(self, msg, *args, extra: dict | None = None, **kwargs):
        self.log_to_loki(msg, "ERROR")
        super().error(msg, *args, **kwargs)

    def exception(self, msg, *args, extra: dict | None = None, **kwargs):
        extra = {**extra, **{"traceback": traceback.format_exc()}}
        self.log_to_loki(msg, "ERROR", extra=extra)
        super().exception(msg, *args, **kwargs)

    def critical(self, msg, *args, extra: dict | None = None, **kwargs):
        self.log_to_loki(msg, "CRITICAL")
        super().critical(msg, *args, **kwargs)


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger.
    """
    if os.environ.get("ENVIRONMENT") == "test":
        logger = logging.Logger(__name__)
    else:
        logger = Logger(__name__, loki_url="http://loki:3100/loki/api/v1/push")
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    return logger


logger = get_logger()
