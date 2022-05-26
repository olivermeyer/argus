import asyncio
from logging import Logger

from src.resources.db import SqliteDbClient, GenericDbClient
from src.resources.discogs import get_wantlist_ids, ListingsPage
from src.resources.logger import logger
from src.resources.telegram import TelegramBot

from aiohttp import ClientSession, TCPConnector


def crawl_async(
        secrets: dict,
        user: str,
        logger: Logger = logger
) -> None:
    """
    Same logic as crawl() but async.
    """
    user_secrets = secrets[user]
    db = SqliteDbClient()
    db.initialize_argus()
    telegram = TelegramBot(secrets["telegram_token"])
    try:
        wantlist_ids = get_wantlist_ids(user_secrets['discogs_token'])
        db.update_wantlist(user=user, release_ids=wantlist_ids)
        logger.info(f"Scanning {len(wantlist_ids)} releases")
        asyncio.run(
            _crawl_async(
                wantlist_ids,
                db,
                telegram,
                user_secrets,
            )
        )
    finally:
        db.close()


async def _crawl_async(
        wantlist_ids: list,
        db: GenericDbClient,
        telegram: TelegramBot,
        user_secrets: dict,
) -> None:
    """
    Awaits for the tasks to finish.
    """
    tasks = []
    connector = TCPConnector(limit=10)
    async with ClientSession(connector=connector) as session:
        for release_id in wantlist_ids:
            tasks.append(_process_release(release_id, db, telegram, user_secrets, session))
        await asyncio.gather(*tasks)


async def _process_release(release_id: str, db, telegram, user_secrets, session):
    """
    Asynchronously processes a single release.
    """
    logger.info(f"Processing release {release_id}")
    discogs_listings = await ListingsPage(release_id).fetch_async(session)
    db_listings = db.get_listing_ids(release_id)
    if db_listings:
        for listing in discogs_listings:
            if listing["id"] not in db_listings:
                logger.info(f"Found new listing: {listing['id']}")
                telegram.send_new_listing_message(
                    user_secrets['telegram_chat_id'],
                    listing
                )
    else:
        logger.debug(f"Release {release_id} not yet in state")
    db.update_listings(
        release_id=release_id,
        listings=discogs_listings,
    )
