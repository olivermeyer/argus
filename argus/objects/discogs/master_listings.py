from dataclasses import dataclass, field
from logging import Logger
from typing import List

from bs4 import BeautifulSoup
from bs4.element import ResultSet

from argus.objects.logger import logger


@dataclass
class MasterListingsPageParser:
    logger: Logger = field(default=logger)

    def parse_listings(self, page_text: str) -> List[dict]:
        self.logger.debug(f"Parsing listings in page:\n{page_text}")
        soup = BeautifulSoup(page_text, "html.parser")
        raw_listings = soup.find_all("tr", {"class": "shortcut_navigable"})
        self.logger.debug(f"Found {len(raw_listings)} listings")
        parsed_listings = []
        for listing in raw_listings:
            parsed_listings.append(self._parse_listing_to_dict(listing))
        return parsed_listings

    def _parse_listing_to_dict(self, listing: ResultSet) -> dict:
        """
        Parses a listing into a dictionary.
        """
        self.logger.debug(f"Parsing listing:\n{listing}")
        item_description_title = listing.find("a", {"class": "item_description_title"})
        title = item_description_title.text
        href = item_description_title.attrs["href"]
        url = f"https://discogs.com{href}"
        listing_id = href.split("/")[-1]
        item_condition = listing.find("p", {"class": "item_condition"})
        media_condition_text = item_condition.find_all("span")[2].text.strip()
        media_condition = self._derive_condition(media_condition_text)
        try:
            sleeve_condition = item_condition.find(
                "span", {"class": "item_sleeve_condition"}
            ).text.strip()
        except AttributeError:
            sleeve_condition = "None"
        seller_info = listing.find("td", {"class": "seller_info"})
        ships_from = seller_info.find_all("li")[2].text.split(":")[-1]
        item_price = listing.find("td", {"class": "item_price"})
        price = item_price.find("span", {"class": "price"}).text
        seller = seller_info.find("div", {"class": "seller_block"}).find("a").text
        return {
            "title": title,
            "url": url,
            "id": listing_id,
            "media_condition": media_condition,
            "sleeve_condition": sleeve_condition,
            "ships_from": ships_from,
            "price": price,
            "seller": seller,
        }

    def _derive_condition(self, text: str) -> str:
        self.logger.debug(f"Deriving condition from text: {text}")
        expected_conditions = [
            "Mint (M)",
            "Near Mint (NM or M-)",
            "Very Good Plus (VG+)",
            "Very Good (VG)",
            "Good (G)",
            "Good Plus (G+)",
            "Poor (P)",
            "Fair (F)",
            "Generic",
        ]
        for condition in expected_conditions:
            if condition in text:
                self.logger.debug(f"Found condition: {condition}")
                return condition
        raise ValueError(f"Couldn't derive a condition from text: {text}")
