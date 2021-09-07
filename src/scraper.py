import logging
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet

from src.logger import logger


class ListingsScraper:
    """
    Class that scrapes listings for a release.
    """
    def __init__(self, logger: logging.Logger = logger):
        self.base_url = "https://discogs.com"
        self.url_parameters = "?sort=listed%2Cdesc&limit=250"
        self.logger = logger

    def get_listings_soup(self, release_id: int) -> ResultSet:
        full_url = f"{self.base_url}" \
                   f"/sell/release/{release_id}" \
                   f"{self.url_parameters}"
        self.logger.info(f"Requesting {full_url}")
        response = requests.get(full_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.find_all("tr", {"class": "shortcut_navigable"})

    def parse_listing(self, listing: ResultSet) -> dict:
        item_description_title = listing.find(
            "a", {"class": "item_description_title"}
        )
        title = item_description_title.text
        href = item_description_title.attrs["href"]
        self.logger.info(f"Parsing listing with URL {self.base_url}{href}")
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
            "href": href,
            "id": listing_id,
            "media_condition": media_condition,
            "sleeve_condition": sleeve_condition,
            "ships_from": ships_from,
            "price": price,
        }

    def scrape(self, release_id: int) -> List[dict]:
        """
        Returns a list of dictionaries with the listings for the release.
        """
        listings = []
        soup_listings = self.get_listings_soup(release_id)
        self.logger.info(f"Found {len(soup_listings)} listings")
        for listing in soup_listings:
            listings.append(self.parse_listing(listing))
        return listings
