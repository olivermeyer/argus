from dataclasses import dataclass, field
from enum import Enum

from bs4 import ResultSet, BeautifulSoup
from currency_symbols import CurrencySymbols

from argus.logger import logger


@dataclass
class _Condition:
    full: str
    long: str
    short: str


class Condition(Enum):
    MINT = _Condition("Mint (M)", "Mint", "M")
    NEAR_MINT = _Condition("Near Mint (NM or M-)", "Near Mint", "NM or M-")
    VERY_GOOD_PLUS = _Condition("Very Good Plus (VG+)", "Very Good Plus", "VG+")
    VERY_GOOD = _Condition("Very Good (VG)", "Very Good", "VG")
    GOOD = _Condition("Good (G)", "Good", "G")
    GOOD_PLUS = _Condition("Good Plus (G+)", "Good Plus", "G+")
    POOR = _Condition("Poor (P)", "Poor", "P")
    FAIR = _Condition("Fair (F)", "Fair", "F")
    GENERIC = _Condition("Generic", "Generic", "Gen")
    NOT_GRADED = _Condition("Not Graded", "Not Graded", "Not Graded")
    NO_COVER = _Condition("No Cover", "No Cover", "No Cover")


@dataclass
class Listing:
    id: str  # TODO: Change this to int
    title: str
    url: str
    media_condition: Condition
    sleeve_condition: Condition
    ships_from: str
    price: float
    currency: str
    seller: str

    def __lt__(self, other: "Listing"):
        return int(self.id) < int(other.id)

    @property
    def price_string(self):
        currency_symbol = CurrencySymbols.get_symbol(self.currency)
        if not currency_symbol:
            raise ValueError(f"Unexpected currency: {self.currency}")
        return f"{currency_symbol}{self.price}"


@dataclass
class ListingsPage:
    html: str
    listings: list[Listing] = field(default_factory=list)

    def __post_init__(self):
        self.listings = self.parse(self.html)

    @staticmethod
    def parse(html: str) -> list[Listing]:
        logger.debug(f"Parsing listings in page:\n{html}")
        soup = BeautifulSoup(html, "html.parser")
        raw_listings = soup.find_all("tr", {"class": "shortcut_navigable"})
        logger.debug(f"Found {len(raw_listings)} listings")
        return [ListingsPage._parse_listing(listing) for listing in raw_listings]

    @staticmethod
    def _parse_listing(listing: ResultSet) -> Listing:
        """Parses a listing."""
        logger.debug(f"Parsing listing:\n{listing}")
        item_description_title = listing.find("a", {"class": "item_description_title"})
        title = item_description_title.text
        href = item_description_title.attrs["href"]
        url = f"https://discogs.com{href}"
        listing_id = href.split("/")[-1]
        item_condition = listing.find("p", {"class": "item_condition"})
        media_condition_text = item_condition.find_all("span")[2].text.strip()
        media_condition = ListingsPage._derive_condition(media_condition_text)
        try:
            sleeve_condition_text = item_condition.find(
                "span", {"class": "item_sleeve_condition"}
            ).text.strip()
            sleeve_condition = ListingsPage._derive_condition(sleeve_condition_text)
        except AttributeError:
            sleeve_condition = Condition.NOT_GRADED
        seller_info = listing.find("td", {"class": "seller_info"})
        ships_from = seller_info.find_all("li")[2].text.split(":")[-1]
        item_price = listing.find("td", {"class": "item_price"})
        price_span = item_price.find("span", {"class": "price"})
        currency = price_span["data-currency"]
        price = float(price_span["data-pricevalue"])
        seller = seller_info.find("div", {"class": "seller_block"}).find("a").text
        return Listing(
            title=title,
            url=url,
            id=listing_id,
            media_condition=media_condition,
            sleeve_condition=sleeve_condition,
            ships_from=ships_from,
            currency=currency,
            price=price,
            seller=seller,
        )

    @staticmethod
    def _derive_condition(text: str) -> Condition:
        logger.debug(f"Deriving condition from text: {text}")
        for condition in Condition:
            if condition.value.full in text:
                logger.debug(f"Found condition: {condition}")
                return condition
        raise ValueError(f"Couldn't derive a condition from text: {text}")
