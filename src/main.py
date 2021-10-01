from src.db import DBClient
from src.discogs import get_wantlist_ids
from src.logger import logger
from src.scraper import ListingsScraper
from src.telegram import send_new_listing_message


def main(secrets, user):
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
    db = DBClient.from_config(secrets["db"])  # TODO: close this connection
    db.initialize_argus()
    while True:
        wantlist_ids = get_wantlist_ids(user_secrets['discogs_token'])
        db.update_wantlist(user=user, release_ids=wantlist_ids)
        logger.info(f"Scanning {len(wantlist_ids)} releases")
        for release_id in wantlist_ids:
            logger.info(f"Processing release {release_id}")
            discogs_listings = ListingsScraper().scrape(release_id)
            db_listings = db.get_listing_ids(release_id)
            if db_listings:
                for listing in discogs_listings:
                    if listing["id"] not in db_listings:
                        logger.info(f"Found new listing: {listing['id']}")
                        send_new_listing_message(
                            user_secrets['telegram_chat_id'],
                            listing
                        )
            else:
                logger.debug(f"Release {release_id} not yet in state")
            db.update_listings(
                release_id=release_id,
                listings=discogs_listings,
            )
