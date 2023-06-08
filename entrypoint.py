import click

# from argus.tasks.task_factory import TaskFactory
from argus.clients.sql.sqlite.client import SqliteClient
from argus.clients.discogs.api.client import DiscogsApiClient
from argus.clients.discogs.web.client import DiscogsWebClient
from argus.clients.telegram.client import TelegramClient
from argus.objects.discogs.release_listings import ReleaseListingsPageParser
from argus.objects.config import get_config
from argus.tasks.crawl_wantlist import CrawlWantlistTask
from argus.tasks.find_non_master_releases_in_list import FindNonMasterReleasesInListTask


@click.group()
def argus():
    pass


@click.command()
@click.option("--user", required=True)
def crawl_wantlist(user: str) -> None:
    config = get_config(user)
    task = CrawlWantlistTask(
        db_client=SqliteClient(),
        discogs_api_client=DiscogsApiClient(token=config["discogs_token"]),
        discogs_web_client=DiscogsWebClient(),
        listings_page_parser=ReleaseListingsPageParser(),
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
            f"[USER: {config['user']}] {e.__class__.__name__}: {str(e)}",
        )
        raise


argus.add_command(crawl_wantlist)


# @click.command()
# @click.option("--user", required=True)
# @click.option("--list_id", required=True)
# @click.option("--sellers", default=10)
# def scrape_list(user: str, list_id: str, sellers: int) -> None:
#     config = get_config(user)
#     task = TaskFactory.create("scrape_list", config=config, list_id=list_id, sellers=sellers)
#     task.execute()


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
