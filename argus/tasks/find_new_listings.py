import asyncio
from time import sleep

from sqlalchemy.engine import Engine

from argus.db import engine as _engine
from argus.discogs.clients.api import DiscogsApiClient
from argus.discogs.clients.web import DiscogsWebClient
from argus.discogs.models.condition import Condition
from argus.discogs.models.listing import Listing, Listings
from argus.discogs.models.wantlist import WantlistItem
from argus.error import Error
from argus.logger import logger
from argus.services.notification import notify_users
from argus.telegram_.client import TelegramClient
from argus.user import User


def find_new_listings(
    telegram: TelegramClient,
    engine: Engine = _engine,
    discogs_api_client: DiscogsApiClient = DiscogsApiClient(),
    discogs_web_client: DiscogsWebClient = DiscogsWebClient(),
):
    logger.info("START - find_new_listings")
    try:
        for user in User.fetch_all(engine=engine):
            WantlistItem.update(user, client=discogs_api_client, engine=engine)
        asyncio.run(
            _process_releases(
                engine=engine, client=discogs_web_client, telegram=telegram
            )
        )
        Listing.clean(engine=engine)
    except Exception as e:
        message = f"Failed to find new listings: {e}"
        logger.error(message)
        notify_users(Error(text=message), engine=engine, telegram=telegram)
    finally:
        logger.info("END - find_new_listings")


async def _process_releases(
    engine: Engine,
    client: DiscogsWebClient,
    telegram: TelegramClient,
) -> None:
    tasks = []
    for release_id in WantlistItem.fetch_all_release_ids(engine=engine):
        tasks.append(
            _process_release(
                release_id=release_id, engine=engine, client=client, telegram=telegram
            )
        )
    for task in asyncio.as_completed(tasks, timeout=10):
        try:
            await task
        except Exception as e:
            message = f"Failed to process release: {e}"
            logger.error(message)
            notify_users(Error(text=message), engine=engine, telegram=telegram)


async def _process_release(
    release_id: int,
    engine: Engine,
    client: DiscogsWebClient,
    telegram: TelegramClient,
) -> None:
    discogs_listings = await Listings.on_discogs(release_id, client=client)
    db_listings = await Listings.in_db(release_id, engine=engine)
    if db_listings:
        if new_listings := [
            listing for listing in discogs_listings if listing not in db_listings
        ]:
            logger.info(
                f"Found {len(new_listings)} new listings for release {release_id}"
            )
            for listing in new_listings:
                notify_users(listing, engine=engine, telegram=telegram)
        else:
            logger.info(f"No new listings for release {release_id}")
    if not discogs_listings:
        discogs_listings = [
            Listing(
                release_id=release_id,
                listing_id=-1,
                title="Dummy release",
                url="http://dummy.com",
                media_condition=Condition.GENERIC,
                sleeve_condition=Condition.GENERIC,
                ships_from="Nowhere",
                price=0,
                currency="EUR",
                seller="Nobody",
            )
        ]
    Listing.update(release_id, discogs_listings, engine=engine)


def main(
    telegram: TelegramClient,
    engine: Engine,
    discogs_api_client: DiscogsApiClient,
    discogs_web_client: DiscogsWebClient,
):
    while True:
        find_new_listings(
            telegram=telegram,
            engine=engine,
            discogs_api_client=discogs_api_client,
            discogs_web_client=discogs_web_client,
        )
        sleep_seconds = 60
        logger.info(f"Sleeping for {sleep_seconds} seconds")
        sleep(sleep_seconds)
