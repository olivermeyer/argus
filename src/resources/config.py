import os
from logging import Logger

from src.resources.logger import logger


config = dict()
config["user"] = os.environ["USER"]
config["discogs_token"] = os.environ["DISCOGS_TOKEN"]
config["telegram_token"] = os.environ["TELEGRAM_TOKEN"]
config["telegram_chat_id"] = os.environ["TELEGRAM_CHAT_ID"]
config["telegram_error_chat_id"] = os.environ["TELEGRAM_ERROR_CHAT_ID"]
