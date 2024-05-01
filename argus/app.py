import asyncio
import os

import click
from sqlmodel import SQLModel

from argus.db import engine
from argus.discogs.clients.api import DiscogsApiClient
from argus.discogs.clients.web import DiscogsWebClient
from argus.tasks.add_user import main as _add_user
from argus.tasks.find_new_listings import main as _find_new_listings
from argus.telegram.client import Telegram


@click.group()
def argus():
    pass


@click.command()
def find_new_listings() -> None:
    asyncio.run(
        _find_new_listings(
            telegram=Telegram(os.environ.get("TELEGRAM_TOKEN")),
            engine=engine,
            discogs_api_client=DiscogsApiClient(),
            discogs_web_client=DiscogsWebClient(),
        )
    )


argus.add_command(find_new_listings)


@click.command()
@click.option("--name", required=True, help="Name of the user.")
@click.option("--discogs_token", required=True, help="Discogs token for the user.")
@click.option(
    "--telegram_chat_id", required=True, help="Telegram chat ID for the user."
)
@click.option(
    "--warn_on_error", default=False, help="Whether to warn the user in case of errors."
)
def add_user(
    name: str,
    discogs_token: str,
    telegram_chat_id: str,
    warn_on_error: bool,
) -> None:
    _add_user(
        name=name,
        discogs_token=discogs_token,
        telegram_chat_id=telegram_chat_id,
        warn_on_error=warn_on_error,
        engine=engine,
    )


argus.add_command(add_user)


def init_db(engine):
    with engine.connect() as connection:
        if not engine.dialect.has_table(connection, "user"):
            SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    init_db(engine)
    argus()
