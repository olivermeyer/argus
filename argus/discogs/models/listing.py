from dataclasses import dataclass, field
from typing import Sequence

from bs4 import BeautifulSoup, ResultSet
from currency_symbols import CurrencySymbols
from sqlalchemy import Engine
from sqlmodel import Field, Session, SQLModel, select

from argus.discogs.clients.web import DiscogsWebClient
from argus.discogs.models.condition import Condition
from argus.logger import logger


class Listing(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    release_id: int = Field(foreign_key="listing.release_id")
    listing_id: int
    title: str
    url: str
    media_condition: Condition
    sleeve_condition: Condition
    ships_from: str
    price: float
    currency: str
    seller: str

    def __lt__(self, other: "Listing"):
        return self.listing_id < other.listing_id

    def __eq__(self, other: "Listing"):
        return self.listing_id == other.listing_id

    @property
    def price_string(self):
        currency_symbol = CurrencySymbols.get_symbol(self.currency)
        if not currency_symbol:
            raise ValueError(f"Unexpected currency: {self.currency}")
        return f"{currency_symbol}{self.price}"

    @staticmethod
    def from_discogs(listing: ResultSet) -> "Listing":
        """Parses a listing."""
        logger.debug(f"Parsing listing:\n{listing}")
        item_description_title = listing.find("a", {"class": "item_description_title"})
        title = item_description_title.text
        href = item_description_title.attrs["href"]
        url = f"https://discogs.com{href}"
        listing_id = href.split("/")[-1]
        item_condition = listing.find("p", {"class": "item_condition"})
        media_condition_text = item_condition.find_all("span")[2].text.strip()
        media_condition = Listing._derive_condition(media_condition_text)
        try:
            sleeve_condition_text = item_condition.find(
                "span", {"class": "item_sleeve_condition"}
            ).text.strip()
            sleeve_condition = Listing._derive_condition(sleeve_condition_text)
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
            listing_id=int(listing_id),
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

    @staticmethod
    def update(release_id: int, listings: list["Listing"], engine: Engine) -> None:
        try:
            logger.info(f"Updating listings for release {release_id} in the database")
            with Session(engine) as session:
                for result in session.exec(
                    select(Listing).where(Listing.release_id == release_id)
                ).all():
                    session.delete(result)
                for listing in listings:
                    session.add(listing)
                session.commit()
        except Exception as e:
            logger.error(f"Failed to update listings for release {release_id}: {e}")
            raise

    @staticmethod
    def clean(engine: Engine) -> None:
        # TODO: implement this
        # delete listings where release_id not in wantlist_item.release_id
        ...


@dataclass
class ListingsPage:
    listings: list[Listing] = field(default_factory=list)

    @staticmethod
    async def fetch(release_id: int, client: DiscogsWebClient) -> "ListingsPage":
        return ListingsPage.from_html(
            await client.get_release_listings_page(release_id=release_id)
        )

    @staticmethod
    def from_html(html: str) -> "ListingsPage":
        logger.debug(f"Parsing listings in page:\n{html}")
        soup = BeautifulSoup(html, "html.parser")
        listings = soup.find_all("tr", {"class": "shortcut_navigable"})
        logger.debug(f"Found {len(listings)} listings")
        return ListingsPage(
            listings=[Listing.from_discogs(listing) for listing in listings]
        )


class Listings:
    @staticmethod
    async def on_discogs(release_id: int, client: DiscogsWebClient) -> list[Listing]:
        listings_page = await ListingsPage.fetch(release_id, client)
        # TODO: do this somewhere else
        for listing in listings_page.listings:
            listing.release_id = release_id
        return listings_page.listings

    @staticmethod
    async def in_db(release_id: int, engine: Engine) -> Sequence[Listing]:
        logger.info(f"Fetching listings for release {release_id} from the database")
        with Session(engine) as session:
            return session.exec(
                select(Listing).where(Listing.release_id == release_id)
            ).all()
