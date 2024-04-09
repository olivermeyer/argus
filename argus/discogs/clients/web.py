from curl_cffi.requests import AsyncSession
from requests import Response

from argus.logger import logger


class DiscogsWebClient:
    async def get_release_listings_page(self, release_id: int) -> str:
        url = f"https://discogs.com/sell/release/{release_id}?sort=listed%2Cdesc&limit=250"
        return await self._get(url)

    async def _get(self, url: str) -> str:
        try:
            logger.debug(f"Getting {url}")
            async with AsyncSession() as session:
                response = await session.get(url=url, impersonate="chrome110")
                response.raise_for_status()
            return response.text
        except Exception as e:
            logger.error(f"Failed to get {url}: {e}")
            raise
