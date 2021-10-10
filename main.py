import argparse

from src.tasks.crawl import crawl
from src.resources.telegram import TelegramBot
from src.resources.secrets import secrets


parser = argparse.ArgumentParser()
parser.add_argument(
    "--user",
    choices=["oli", "pa", "ash"],
    required=True,
)


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        crawl(
            secrets=secrets,
            user=args.user,
        )
    except Exception as e:
        telegram = TelegramBot(secrets["telegram_token"])
        telegram.send_message(
            secrets["error_chat_id"],
            f"[USER: {args.user}] {e.__class__.__name__}: {str(e)}"
        )
        raise
