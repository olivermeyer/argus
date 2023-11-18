import asyncio
from collections import defaultdict
from dataclasses import dataclass
from logging import Logger
from typing import List

from argus.clients.discogs.api import DiscogsApiClient
from argus.clients.discogs.web import DiscogsWebClient
from argus.models.discogs import ListingsPage
from argus.logger import logger


@dataclass
class ScrapeListTask:
    """
    This task is used to find the sellers with the highest number of listings for the releases in a list.

    TODO: this gets listings for releases, not masters
    """
    discogs_api_client: DiscogsApiClient
    discogs_web_client: DiscogsWebClient
    list_id: int
    sellers: int
    logger: Logger = logger

    def execute(self):
        release_ids = self._get_list_release_ids(list_id=self.list_id)
        sellers = defaultdict(int)
        listings = asyncio.run(self._execute_async(release_ids))
        listings = [listing for sublist in listings for listing in sublist]
        for listing in listings:
            sellers[listing["seller"]] += 1
        sellers = {k: {"items": v, "url": f"https://www.discogs.com/seller/{k}/profile"} for k, v in sellers.items()}
        sorted_sellers = sorted(sellers.items(), key=lambda x: x[1]["items"], reverse=True)
        for seller in sorted_sellers[:self.sellers]:
            print(seller[0])
            print(f"  url: {seller[1]['url']}")
            print(f"  items: {seller[1]['items']}")

    def _get_list_release_ids(self, list_id: int) -> List[int]:
        """
        Returns the IDs in the list.
        """
        self.logger.info(f"Fetching releases in list {list_id}")
        return [item.id for item in self.discogs_api_client.list(list_id).items]

    async def _execute_async(self, release_ids):
        tasks = []
        for release_id in release_ids:
            tasks.append(
                self._get_listings_for_release(
                    release_id
                )
            )
        return await asyncio.gather(*tasks)

    async def _get_listings_for_release(self, release_id):
        self.logger.info(f"Processing release {release_id}")
        listings = ListingsPage(
            html=await self.discogs_web_client.get_master_listings_page(master_id=release_id)
        )
        return listings
