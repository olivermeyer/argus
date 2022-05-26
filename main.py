import argparse

from src.tasks.crawl import crawl
from src.tasks.crawl_async import crawl_async
from src.resources.telegram import TelegramBot
from src.resources.secrets import secrets


parser = argparse.ArgumentParser()
parser.add_argument(
    "--user",
    choices=["oli", "pa", "ash"],
    required=True,
)
parser.add_argument(
    "--asynchronous",
    type=bool,
    required=True,
)


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        if args.asynchronous:
            crawl_async(
                secrets=secrets,
                user=args.user,
            )
        else:
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
