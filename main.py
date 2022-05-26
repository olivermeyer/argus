import argparse

from src.tasks.task_factory import TaskFactory
from src.resources.telegram import TelegramBot
from src.resources.secrets import secrets


parser = argparse.ArgumentParser()
parser.add_argument(
    "--user",
    choices=["oli", "pa", "ash"],
    required=True,
)
parser.add_argument(
    "--task",
    choices=["crawl", "crawl_async"],
    required=True,
)


if __name__ == "__main__":
    args = parser.parse_args()
    task = TaskFactory.create(args.task, user=args.user, secrets=secrets)
    try:
        task.execute()
    except Exception as e:
        telegram = TelegramBot(secrets["telegram_token"])
        telegram.send_message(
            secrets["error_chat_id"],
            f"[USER: {args.user}] {e.__class__.__name__}: {str(e)}"
        )
        raise
