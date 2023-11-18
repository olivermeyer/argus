import traceback

import click

from argus.clients.sql.sqlite import SqliteClient
from argus.clients.discogs.api import DiscogsApiClient
from argus.clients.discogs.web import DiscogsWebClient
from argus.clients.telegram import TelegramClient
from argus.config import get_config
from argus.tasks.find_new_listings import FindNewListingsTask
from argus.tasks.find_non_master_releases_in_list import FindNonMasterReleasesInListTask
from argus.tasks.scrape_list import ScrapeListTask


@click.group()
def argus():
    pass


@click.command()
@click.option("--user", required=True)
def find_new_listings(user: str) -> None:
    config = get_config(user)
    task = FindNewListingsTask(
        db_client=SqliteClient(),
        discogs_api_client=DiscogsApiClient(token=config["discogs_token"]),
        discogs_web_client=DiscogsWebClient(),
        telegram_client=TelegramClient(
            token=config["telegram_token"], chat_id=config["telegram_chat_id"]
        ),
        user=config["user"],
    )
    try:
        task.execute()
    except Exception as e:
        telegram_client = TelegramClient(
            token=config["telegram_token"],
            chat_id=config["telegram_chat_id_errors"],
        )
        telegram_client.bot.send_message(
            config["telegram_chat_id_errors"],
            f"[USER: {config['user']}]\n{traceback.format_exc()}",
        )
        raise


argus.add_command(find_new_listings)


@click.command()
@click.option("--user", required=True)
@click.option("--list_id", required=True)
@click.option("--sellers", default=10)
def scrape_list(user: str, list_id: int, sellers: int) -> None:
    config = get_config(user)
    task = ScrapeListTask(
        discogs_api_client=DiscogsApiClient(token=config["discogs_token"]),
        discogs_web_client=DiscogsWebClient(),
        list_id=list_id,
        sellers=sellers,
    )
    task.execute()


argus.add_command(scrape_list)


@click.command()
@click.option("--user", required=True)
def clean_lists(user: str) -> None:
    config = get_config(user)
    task = FindNonMasterReleasesInListTask(
        discogs_api_client=DiscogsApiClient(token=config["discogs_token"])
    )
    task.execute()


argus.add_command(clean_lists)


if __name__ == "__main__":
    argus()
