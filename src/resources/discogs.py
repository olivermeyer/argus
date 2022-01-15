import requests
from json import JSONDecodeError
from logging import Logger
from typing import List

import discogs_client
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from requests.exceptions import HTTPError
from requests.exceptions import ChunkedEncodingError
from requests.exceptions import ConnectionError
from retry import retry

from src.resources.logger import logger


# user.wantlist can raise JSONDecodeError
@retry(
    exceptions=JSONDecodeError,
    delay=1,
    tries=3,
    backoff=2,
    logger=logger,
)
def get_wantlist_ids(
        discogs_token: str,
        page_size: int = 100,
        logger: Logger = logger
) -> List[str]:
    """
    Returns the IDs in the wantlist for the account linked to the token.
    """
    logger.info("Fetching wantlist")
    discogs = discogs_client.Client(
        user_agent="Argus",
        user_token=discogs_token
    )
    user = discogs.identity()
    wantlist = user.wantlist
    wantlist.per_page = page_size
    return [str(item.id) for item in wantlist]


class ListingsPage:
    """
    This class represents a Discogs listings page.

    It's main entrypoint is fetch(), which returns a listings page parsed
    into a list of dictionaries, where each dictionary represents a listing.
    """
    def __init__(self, logger: Logger = logger):
        self.base_url = "https://discogs.com"
        self.url_parameters = "?sort=listed%2Cdesc&limit=250"
        self.logger = logger

    @retry(
        exceptions=(HTTPError, ChunkedEncodingError, ConnectionError),
        delay=1,
        tries=3,
        backoff=2,
        logger=logger,
    )
    def get_listings_from_discogs(self, release_id: str) -> ResultSet:
        """
        Gets ResultsSet containing the listings for the release.
        """
        full_url = f"{self.base_url}" \
                   f"/sell/release/{release_id}" \
                   f"{self.url_parameters}"
        self.logger.debug(f"Requesting {full_url}")
        response = requests.get(full_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("tr", {"class": "shortcut_navigable"})

    def parse_listing_to_dict(self, listing: ResultSet) -> dict:
        """
        Parses a listing into a dictionary.
        """
        item_description_title = listing.find(
            "a", {"class": "item_description_title"}
        )
        title = item_description_title.text
        href = item_description_title.attrs["href"]
        url = f"{self.base_url}{href}"
        self.logger.debug(f"Parsing listing with URL {url}")
        listing_id = href.split("/")[-1]
        item_condition = listing.find("p", {"class": "item_condition"})
        media_condition = item_condition.find_all("span")[2].text.strip()
        try:
            sleeve_condition = item_condition.find_all("span")[5].text.strip()
        except IndexError:
            sleeve_condition = "None"
        seller_info = listing.find("td", {"class": "seller_info"})
        ships_from = seller_info.find_all("li")[2].text.split(":")[-1]
        item_price = listing.find("td", {"class": "item_price"})
        price = item_price.find("span", {"class": "price"}).text
        return {
            "title": title,
            "url": url,
            "id": listing_id,
            "media_condition": media_condition,
            "sleeve_condition": sleeve_condition,
            "ships_from": ships_from,
            "price": price,
        }

    def fetch(self, release_id: str) -> List[dict]:
        """
        Returns a list of dictionaries with the listings for the release.
        """
        listings = []
        raw_listings = self.get_listings_from_discogs(release_id)
        self.logger.debug(f"Found {len(raw_listings)} listings")
        for listing in raw_listings:
            listings.append(self.parse_listing_to_dict(listing))
        return listings
