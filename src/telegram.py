import os
from logging import Logger

import requests
import yaml

from src.helpers import abbreviate_condition
from src.logger import logger


with open(f"{os.environ['ARGUS_DIRECTORY']}/secrets.yaml", "r") as fh:
    secrets = yaml.safe_load(fh)


def send_new_listing_message(listing: dict) -> None:
    send_message(
        text=prepare_new_listing_message(listing)
    )


def send_failure_message(text: str) -> None:
    send_message(clean_string(text))


def send_message(text: str, logger: Logger = logger) -> None:
    logger.info(f"Sending message with text {text}")
    url = \
        f"https://api.telegram.org/bot{secrets['telegram_token']}/sendMessage"
    params = {
        "chat_id": secrets["telegram_chat_id"],
        "text": text,
        "parse_mode": "MarkdownV2",
    }
    r = requests.get(url, params=params)
    r.raise_for_status()


def prepare_new_listing_message(listing: dict) -> str:
    short_media_condition = abbreviate_condition(listing["media_condition"])
    short_sleeve_condition = abbreviate_condition(listing["sleeve_condition"])
    first_line = f"*{clean_string(listing['title'])}*"
    second_line = f"{clean_string(short_media_condition)} / " \
                  f"{clean_string(short_sleeve_condition)} \| " \
                  f"{clean_string(listing['price'])} \| " \
                  f"{clean_string(listing['ships_from'])}"
    third_line = f"View on [Discogs]({listing['url']})"
    return f"{first_line}\n{second_line}\n{third_line}"


def clean_string(string):
    return string.replace(
        "-", "\-"
    ).replace(
        "(", "\("
    ).replace(
        ")", "\)"
    ).replace(
        ".", "\."
    ).replace(
        "+", "\+"
    ).replace(
        "*", ""
    ).replace(
        "=", "\="
    ).replace(
        ":", "\:"
    )
