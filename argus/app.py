import click

from sqlmodel import SQLModel

from argus.db import engine
from argus.discogs.clients.api import DiscogsApiClient
from argus.discogs.clients.web import DiscogsWebClient
from argus.tasks.find_new_listings import main
from argus.telegram_.client import TelegramClient


@click.group()
def argus():
    pass


@click.command()
def find_new_listings() -> None:
    main(
        telegram=TelegramClient("1997819840:AAFlb7dYUy6m6hl0VIEiQHPWNx3laid2zKI"),
        engine=engine,
        discogs_api_client=DiscogsApiClient(),
        discogs_web_client=DiscogsWebClient(),
    )


def init_db(engine):
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, "user"):
            SQLModel.metadata.create_all(engine)


argus.add_command(find_new_listings)


if __name__ == "__main__":
    init_db(engine)
    argus()
