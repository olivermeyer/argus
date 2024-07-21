from curl_cffi import CurlHttpVersion
from curl_cffi.requests import AsyncSession

from argus.logger import logger


class DiscogsWebClient:
    async def get_release_listings_page(self, release_id: int) -> str:
        url = f"https://discogs.com/sell/release/{release_id}?sort=listed%2Cdesc&limit=250"
        return await self._get(url)

    # Retries seem to cause a lot of 403 errors, disabling them to confirm
    # @retry(tries=3, delay=1, backoff=1, logger=logger, is_async=True)
    async def _get(self, url: str) -> str:
        try:
            logger.info(f"GET {url}")
            async with AsyncSession(http_version=CurlHttpVersion.V1_1) as session:
                response = await session.get(url=url, impersonate="chrome110")
                response.raise_for_status()
            return response.text
        except Exception:
            logger.exception(f"Failed to GET {url}")
            raise
