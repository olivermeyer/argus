import asyncio
from dataclasses import dataclass
from json import JSONDecodeError
from logging import Logger

from argus.clients.sql.generic.client import GenericSqlClient
from argus.clients.discogs.api.client import DiscogsApiClient
from argus.clients.discogs.web.client import DiscogsWebClient
from argus.clients.telegram.client import TelegramClient
from argus.models.discogs.listing import Listing, ListingsPage
from argus.logger import logger


@dataclass
class CrawlWantlistTask:
    db_client: GenericSqlClient
    discogs_api_client: DiscogsApiClient
    discogs_web_client: DiscogsWebClient
    telegram_client: TelegramClient
    user: str
    logger: Logger = logger

    def execute(self):
        """
        Crawls a user's wantlist to find new listings.
        """
        self.db_client.initialize_argus()
        try:
            wantlist_ids = self.discogs_api_client.get_wantlist_ids()
            self.db_client.update_wantlist(user=self.user, release_ids=wantlist_ids)
            asyncio.run(
                self._crawl_async(
                    wantlist_ids,
                )
            )
        except JSONDecodeError:
            self.logger.error("JSONDecodeError while getting wantlist")
        finally:
            self.db_client.close()

    async def _crawl_async(
        self,
        wantlist_ids: list,
    ):
        """
        Creates one async task for each release in the wantlist and gathers the results.
        """
        tasks = []
        for release_id in wantlist_ids:
            tasks.append(
                self._process_release(
                    release_id
                )
            )
        await asyncio.gather(*tasks)

    async def _process_release(
        self,
        release_id: str,
    ):
        """
        Asynchronously processes a single release.
        """
        self.logger.info(f"Processing release {release_id}")
        discogs_listings = ListingsPage.from_html(
            html=await self.discogs_web_client.get_release_listings_page(release_id=release_id)
        )
        db_listings = self.db_client.get_listing_ids(release_id)
        if db_listings:
            self._process_existing_release(discogs_listings=discogs_listings.listings, db_listings=db_listings)
        else:
            self._process_new_release(release_id=release_id)
        self.db_client.update_listings(
            release_id=release_id,
            listings=discogs_listings.listings,
        )

    def _process_existing_release(self, discogs_listings: list[Listing], db_listings: list[str]) -> None:
        """
        Compares listings from Discogs with listings from the DB.

        If a new listing is found, sends a message to Telegram.
        """
        for discogs_listing in discogs_listings:
            if discogs_listing.id not in db_listings:
                self.logger.info(f"Found new listing: {discogs_listing.id}")
                self.telegram_client.send_new_listing_message(discogs_listing)

    def _process_new_release(self, release_id: str) -> None:
        """
        Logs the new release and does nothing.
        """
        self.logger.debug(f"Release {release_id} not yet in state")
