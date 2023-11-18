from dataclasses import dataclass, field
from logging import Logger

from argus.clients.http.client import HttpClient
from argus.logger import logger


@dataclass
class DiscogsWebClient:
    http_client: HttpClient = field(default=HttpClient())
    logger: Logger = logger

    async def get_release_listings_page(self, release_id: str) -> str:
        url = f"https://discogs.com/sell/release/{release_id}?sort=listed%2Cdesc&limit=250"
        return await self._get(url)

    async def get_master_listings_page(self, master_id: str) -> str:
        # TODO: this gets listings for a release, not for a master
        url = f"https://discogs.com/sell/release/{master_id}?sort=listed%2Cdesc&limit=250"
        return await self._get(url)

    async def _get(self, url: str) -> str:
        self.logger.debug(f"Getting {url}")
        response = await self.http_client.get(url=url, headers={"User-Agent": "Mozilla/5.0"})
        return response
