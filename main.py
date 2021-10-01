import argparse

from src.main import main
from src.telegram import send_message
from src.secrets import secrets


parser = argparse.ArgumentParser()
parser.add_argument(
    "--user",
    choices=["oli", "pa"],
    required=True,
)


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        main(
            secrets=secrets,
            user=args.user,
        )
    except Exception as e:
        send_message(secrets['oli']['telegram_chat_id'], str(e))
        raise
