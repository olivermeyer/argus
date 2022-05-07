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
    BASE_URL = "https://discogs.com"
    URL_PARAMETERS = "?sort=listed%2Cdesc&limit=250"

    def __init__(self, release_id: str, logger: Logger = logger):
        self.release_id = release_id
        self.logger = logger
        self.raw_listings = None
        self.listings = []

    @property
    def url(self):
        return f"{ListingsPage.BASE_URL}" \
               f"/sell/release/{self.release_id}" \
               f"{ListingsPage.URL_PARAMETERS}"

    @retry(
        exceptions=(HTTPError, ChunkedEncodingError, ConnectionError),
        delay=1,
        tries=3,
        backoff=2,
        logger=logger,
    )
    def _fetch_listings_from_discogs(self):
        """
        Gets ResultsSet containing the listings for the release.
        """
        self.logger.debug(f"Requesting {self.url}")
        response = requests.get(
            self.url, headers={'User-Agent': 'Mozilla/5.0'}
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        self.raw_listings = soup.find_all(
            "tr", {"class": "shortcut_navigable"}
        )
        self.logger.debug(f"Found {len(self.raw_listings)} listings")

    def _parse_listings_to_dicts(self):
        for listing in self.raw_listings:
            self.logger.debug(f"Parsing listing:\n{listing}")
            self.listings.append(
                self._parse_listing_to_dict(listing)
            )

    @staticmethod
    def _parse_listing_to_dict(listing: ResultSet) -> dict:
        """
        Parses a listing into a dictionary.
        """
        item_description_title = listing.find(
            "a", {"class": "item_description_title"}
        )
        title = item_description_title.text
        href = item_description_title.attrs["href"]
        url = f"{ListingsPage.BASE_URL}{href}"
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

    def fetch(self) -> List[dict]:
        """
        Returns a list of dictionaries with the listings for the release.
        """
        self._fetch_listings_from_discogs()
        self._parse_listings_to_dicts()
        return self.listings
