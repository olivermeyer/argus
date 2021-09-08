import os

from src.logger import logger
from src.scraper import ListingsScraper
from src.state import read_state, write_state
from src.telegram import send_new_listing_message


RELEASE_IDS = [
    "4504379",
    "7237693",
    "7248670",
    "7544386",
    "8044643",
    "9796117",
    "10711117",
    "11497334",
    "14100916",
    "14355421",
    "15260825",
    "15350761",
    "15350980",
    "11830308",
    "1484030",
    "10300882",
    "11793980",
    "4870292",
    "11770297",
    "7429346",
    "4918656",
    "13743851",
    "2607649",
    "7167416",
    "3757676",
    "7998269",
    "5325496",
    "12273825",
    "12776226",
    "233588",
]


if __name__ == "__main__":
    # General idea:
    # Loop over all release IDs in the wantlist; for each:
    #   * Get current listings from Discogs
    #   * If the release ID is not yet in the listing state, then skip
    #     to the bottom
    #   * If the release ID is in the listing state, then for each current
    #     listing, check whether it's in the state. If not, it's a new
    #     listing!
    #   * Write the current listings for the release to the state
    while True:
        logger.info(f"Scanning {len(RELEASE_IDS)} releases")
        for release_id in RELEASE_IDS:
            current_listings = ListingsScraper().scrape(release_id)
            listings_state = read_state(
                f"{os.environ['STATE_DIRECTORY']}/listings.json"
            )
            if release_id in listings_state:
                for listing in current_listings:
                    if listing["id"] not in listings_state[release_id]:
                        send_new_listing_message(listing)
            else:
                logger.info(f"Release {release_id} not yet in state")
            listings_state[release_id] = [
                listing["id"] for listing in current_listings
            ]
            write_state(
                listings_state,
                f"{os.environ['STATE_DIRECTORY']}/listings.json"
            )
