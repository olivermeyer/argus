import argparse

from src.tasks.task_factory import TaskFactory
from src.resources.telegram import TelegramBot
from src.resources.config import config


parser = argparse.ArgumentParser()
parser.add_argument(
    "--task",
    choices=["crawl_async"],
    required=True,
)


if __name__ == "__main__":
    args = parser.parse_args()
    task = TaskFactory.create(args.task, config=config)
    try:
        task.execute()
    except Exception as e:
        telegram = TelegramBot(config["telegram_token"])
        telegram.send_message(
            config["telegram_chat_id_errors"],
            f"[USER: {config['user']}] {e.__class__.__name__}: {str(e)}",
        )
        raise
