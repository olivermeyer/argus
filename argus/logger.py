import json
import logging
import os
import time
import traceback
from typing import Any

import requests


class Logger(logging.Logger):
    DEFAULT_LABELS = {
        "application": "argus",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.loki_url = kwargs.get("loki_url", None)
        self.labels = Logger.DEFAULT_LABELS

    def _stringify_values(self, data: dict[str, Any]) -> dict[str, str]:
        return {key: str(value) for key, value in data.items()}

    def log_to_loki(self, msg, level: str, extra: dict | None = None):
        extra = {**self.labels, **extra} if extra else self.labels
        payload = {
            "streams": [
                {
                    "stream": Logger.DEFAULT_LABELS,
                    "values": [
                        [
                            str(time.time_ns()),
                            f"[{level}] {msg}",
                            self._stringify_values(extra),
                        ]
                    ],
                }
            ]
        }
        headers = {"Content-type": "application/json"}
        payload = json.dumps(payload)
        response = requests.post(self.loki_url, data=payload, headers=headers)
        response.raise_for_status()

    def info(self, msg, *args, extra: dict | None = None, **kwargs):
        if self.loki_url:
            self.log_to_loki(msg, "INFO", extra=extra)
        super().info(msg, *args, **kwargs)

    def debug(self, msg, *args, extra: dict | None = None, **kwargs):
        # if self.loki_url:
        #   self.log_to_loki(msg, "DEBUG")
        super().debug(msg, *args, **kwargs, extra=extra)

    def warning(self, msg, *args, extra: dict | None = None, **kwargs):
        if self.loki_url:
            self.log_to_loki(msg, "WARNING")
        super().warning(msg, *args, **kwargs, extra=extra)

    def error(self, msg, *args, extra: dict | None = None, **kwargs):
        if self.loki_url:
            self.log_to_loki(msg, "ERROR")
        super().error(msg, *args, **kwargs, extra=extra)

    def exception(self, msg, *args, extra: dict | None = None, **kwargs):
        extra = (
            {**extra, **{"traceback": traceback.format_exc()}}
            if extra
            else {"traceback": traceback.format_exc()}
        )
        if self.loki_url:
            self.log_to_loki(msg, "ERROR", extra=extra)
        super().exception(msg, *args, **kwargs)

    def critical(self, msg, *args, extra: dict | None = None, **kwargs):
        if self.loki_url:
            self.log_to_loki(msg, "CRITICAL")
        super().critical(msg, *args, **kwargs)

    def add_labels(self, **kwargs):
        self.labels = {
            **self.labels,
            **kwargs,
        }

    def clear_labels(self):
        self.labels = Logger.DEFAULT_LABELS


def get_logger() -> logging.Logger:
    """
    Configures and returns a logger.
    """
    if os.environ.get("ENVIRONMENT") == "test":
        logger = Logger(__name__)
    else:
        logger = Logger(__name__, loki_url="http://loki:3100/loki/api/v1/push")
    logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))
    stream_handler = logging.StreamHandler()
    logger.addHandler(stream_handler)
    return logger


logger = get_logger()
