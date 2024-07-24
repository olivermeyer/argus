from curl_cffi import CurlHttpVersion
from curl_cffi.requests import AsyncSession
from retry_async import retry

from argus.logger import logger


class DiscogsWebClient:
    async def get_release_listings_page(self, release_id: int) -> str:
        url = f"https://discogs.com/sell/release/{release_id}?sort=listed%2Cdesc&limit=250"
        return await self._get(url)

    @retry(tries=3, delay=5, backoff=2, logger=logger, is_async=True)
    async def _get(self, url: str) -> str:
        try:
            logger.info(f"GET {url}")
            async with AsyncSession() as session:
                response = await session.get(url=url, impersonate="chrome110")
                response.raise_for_status()
            return response.text
        except Exception:
            logger.exception(f"Failed to GET {url}", response=response.text)
            raise
