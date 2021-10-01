import os
import argparse

from src.db import DBClient
from src.discogs import get_wantlist_ids
from src.logger import logger
from src.scraper import ListingsScraper
from src.state import read_state, write_state
from src.telegram import send_new_listing_message, send_message
from src.secrets import secrets


parser = argparse.ArgumentParser()
parser.add_argument(
    "--user",
    choices=["oli", "pa"],
    required=True,
)


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
    db = DBClient.from_config(secrets["db"])
    db.initialize_argus()
    while True:
        wantlist_ids = get_wantlist_ids(user_secrets['discogs_token'])
        logger.info(f"Scanning {len(wantlist_ids)} releases")
        for release_id in wantlist_ids:
            logger.info(f"Processing release {release_id}")
            current_listings = ListingsScraper().scrape(release_id)
            listings_state = read_state(
                f"{os.environ['STATE_DIRECTORY']}/listings.json"
            )
            if release_id in listings_state:
                for listing in current_listings:
                    if listing["id"] not in listings_state[release_id]:
                        logger.info(f"Found new listing: {listing['id']}")
                        send_new_listing_message(
                            user_secrets['telegram_chat_id'],
                            listing
                        )
            else:
                logger.debug(f"Release {release_id} not yet in state")
            listings_state[release_id] = [
                listing["id"] for listing in current_listings
            ]
            write_state(
                listings_state,
                f"{os.environ['STATE_DIRECTORY']}/listings.json"
            )


if __name__ == "__main__":
    args = parser.parse_args()
    try:
        main(
            secrets=secrets,
            user=args.user,
        )
    except Exception as e:
        send_message(secrets['oli']['telegram_chat_id'], str(e))
        raise
