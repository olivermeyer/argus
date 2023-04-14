import asyncio
from collections import defaultdict
from typing import List

from aiohttp import ClientSession, TCPConnector

from argus.resources.discogs import ListingsPage
from argus.tasks.abstract import AbstractTask


class ScrapeListTask(AbstractTask):
    """
    This task is used to find the sellers with the highest number of listings for the releases in a list.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_id = self.kwargs["list_id"]
        self.sellers = self.kwargs["sellers"]

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
        return [item.id for item in self.discogs_client.list(list_id).items]

    async def _execute_async(self, release_ids):
        tasks = []
        connector = TCPConnector(limit=50)
        async with ClientSession(connector=connector) as session:
            for release_id in release_ids:
                tasks.append(
                    self._get_listings_for_release(
                        release_id, session
                    )
                )
            return await asyncio.gather(*tasks)

    async def _get_listings_for_release(self, release_id, session):
        self.logger.info(f"Processing release {release_id}")
        listings = await ListingsPage(release_id).fetch_async(session)
        return listings
