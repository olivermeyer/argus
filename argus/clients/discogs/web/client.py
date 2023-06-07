from dataclasses import dataclass, field
from logging import Logger

from argus.clients.http.client import HttpClient
from argus.objects import logger


@dataclass
class DiscogsWebClient:
    http_client: HttpClient = field(default=HttpClient())
    logger: Logger = logger

    async def get_listings_page(self, release_id: str) -> str:
        url = f"https://discogs.com/sell/release/{release_id}?sort=listed%2Cdesc&limit=250"
        self.logger.debug(f"Get listings from {url}")
        response = await self.http_client.get(url=url, headers={"User-Agent": "Mozilla/5.0"})
        return response
