import os

from src.scraper import ListingsScraper
from src.state import read_state, write_state
from src.logger import logger
from src.helpers import get_new_listing_ids


RELEASE_IDS = [
    # "4504379",
    # "7237693",
    # "7248670",
    # "7544386",
    # "8044643",
    # "9796117",
    # "10711117",
    # "11497334",
    # "14100916",
    # "14355421",
    # "15260825",
    # "15350761",
    # "15350980",
    # "11830308",
    # "1484030",
    # "10300882",
    # "11793980",
    # "4870292",
    # "11770297",
    # "7429346",
    # "4918656",
    # "13743851",
    # "2607649",
    # "7167416",
    # "3757676",
    # "7998269",
    # "5325496",
    # "12273825",
    # "12776226",
    # "233588",
    "17331661",
]


if __name__ == "__main__":
    while True:
        logger.info(f"Scanning {len(RELEASE_IDS)} releases")
        for release_id in RELEASE_IDS:
            current_listings = ListingsScraper().scrape(release_id)
            current_listing_ids = [
                listing["listing_id"] for listing in current_listings
            ]
            listings_state = read_state(
                f"{os.environ['STATE_DIRECTORY']}/listings.json"
            )
            if release_id in listings_state:
                # If the relase ID does not appear in the listings state
                # then this is the first run for that release, so we
                # do not send out notifications.
                old_listing_ids = listings_state.get(release_id)
                new_listings_ids = get_new_listing_ids(
                    current_listing_ids, old_listing_ids
                )
                if new_listings_ids:
                    print("#### NEW LISTINGS!!! ALERT!!! ####")
            else:
                logger.info(f"Release {release_id} not yet in state")
            listings_state[release_id] = current_listing_ids
            write_state(
                listings_state,
                f"{os.environ['STATE_DIRECTORY']}/listings.json"
            )
