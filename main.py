import argparse

from src.entrypoint import entrypoint
from src.telegram import TelegramBot
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
        entrypoint(
            secrets=secrets,
            user=args.user,
        )
    except Exception as e:
        telegram = TelegramBot(secrets["telegram_token"])
        telegram.send_message(
            secrets["error_chat_id"],
            f"Exception for user {args.user}: {str(e)}"
        )
        raise
