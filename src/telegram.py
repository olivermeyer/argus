import os

import requests
import yaml


with open(f"{os.environ['ARGUS_DIRECTORY']}/secrets.yaml", "r") as fh:
    secrets = yaml.safe_load(fh)


def send_message(text: str, chat_id: int) -> None:
    url = f"https://api.telegram.org/" \
          f"bot{secrets['telegram_token']}/" \
          f"sendMessage?chat_id={chat_id}&text={text}"
    r = requests.get(url)
    r.raise_for_status()
