from logging import Logger

from src.resources.db import SqliteDbClient
from src.resources.discogs import get_wantlist_ids, ListingsPage
from src.resources.logger import logger
from src.resources.telegram import TelegramBot


def crawl(
        secrets: dict,
        user: str,
        logger: Logger = logger
) -> None:
    """
    General idea:
    First, initialize the DB.
    Then, loop over all release IDs in the wantlist; for each:
      * Get current listings from Discogs
      * If the release ID is not yet in the listing state, then skip
        to the bottom
      * If the release ID is in the listing state, then for each current
        listing, check whether it's in the state. If not, it's a new
        listing!
      * Write the current listings for the release to the state
    """
    user_secrets = secrets[user]
    db = SqliteDbClient()
    db.initialize_argus()
    telegram = TelegramBot(secrets["telegram_token"])
    try:
        while True:
            wantlist_ids = get_wantlist_ids(user_secrets['discogs_token'])
            db.update_wantlist(user=user, release_ids=wantlist_ids)
            logger.info(f"Scanning {len(wantlist_ids)} releases")
            for release_id in wantlist_ids:
                logger.info(f"Processing release {release_id}")
                discogs_listings = ListingsPage().fetch(release_id)
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
    finally:
        db.close()
