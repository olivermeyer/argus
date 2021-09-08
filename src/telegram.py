import os

import requests
import yaml


with open(f"{os.environ['ARGUS_DIRECTORY']}/secrets.yaml", "r") as fh:
    secrets = yaml.safe_load(fh)


def send_new_listing_message(listing: dict) -> None:
    send_message(
        text=prepare_new_listing_message(listing)
    )


def send_failure_message(text: str) -> None:
    send_message(clean_string(text))


def send_message(text: str) -> None:
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
    return f"""
*{clean_string(listing['title'])}*
{clean_string(listing['media_condition'])} / {clean_string(listing['sleeve_condition'])}
{clean_string(listing['price'])} \({clean_string(listing['ships_from'])}\)
See on [Discogs]({listing["url"]})"""


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
    )
