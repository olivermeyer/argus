import click

from argus.tasks.task_factory import TaskFactory
from argus.resources.telegram import TelegramBot
from argus.resources.config import get_config


@click.group()
def argus():
    pass


@click.command()
@click.option("--user", required=True)
def crawl_wantlist(user: str) -> None:
    config = get_config(user)
    task = TaskFactory.create("crawl_wantlist", config=config)
    try:
        task.execute()
    except Exception as e:
        telegram = TelegramBot(config["telegram_token"])
        telegram.send_message(
            config["telegram_chat_id_errors"],
            f"[USER: {config['user']}] {e.__class__.__name__}: {str(e)}",
        )
        raise


@click.command()
@click.option("--user", required=True)
@click.option("--list_id", required=True)
@click.option("--sellers", default=10)
def scrape_list(user: str, list_id: str, sellers: int) -> None:
    config = get_config(user)
    task = TaskFactory.create("scrape_list", config=config, list_id=list_id, sellers=sellers)
    task.execute()


@click.command()
@click.option("--user", required=True)
def clean_lists(user: str) -> None:
    config = get_config(user)
    task = TaskFactory.create("clean_lists", config=config)
    task.execute()


argus.add_command(crawl_wantlist)
argus.add_command(scrape_list)
argus.add_command(clean_lists)

if __name__ == "__main__":
    argus()
