from logging import Logger

import requests
from requests.exceptions import HTTPError

from src.helpers import abbreviate_condition
from src.logger import logger
from src.secrets import secrets


def send_new_listing_message(chat_id: int, listing: dict) -> None:
    try:
        send_message(
            chat_id=chat_id,
            text=prepare_new_listing_message(listing)
        )
    except HTTPError:
        send_message(
            chat_id=secrets['oli']['telegram_chat_id'],
            text=f"Failed to send new listing {listing['id']} to {chat_id}"
        )
        raise


def send_message(chat_id: int, text: str, logger: Logger = logger) -> None:
    logger.debug(f"Sending message with text {text}")
    url = \
        f"https://api.telegram.org/bot{secrets['telegram_token']}/sendMessage"
    params = {
        "chat_id": chat_id,
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


def clean_string(string: str) -> str:
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
