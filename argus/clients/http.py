from dataclasses import dataclass
from logging import Logger

from curl_cffi.requests import AsyncSession

from argus.logger import logger


@dataclass
class HttpClient:
    """
    Wrapper class for making asynchronous HTTP requests.
    """
    logger: Logger = logger

    async def get(self, **kwargs) -> str:
        """
        Makes a GET request with the received kwargs and returns the response text.

        Uses the RetryClient to automatically retry exceptions.
        Any exception thrown by the last attempt is raised.
        """
        self.logger.debug(f"Sending get request with kwargs: {kwargs}")
        async with AsyncSession() as session:
            response = await session.get(**{**kwargs, **{"impersonate": "chrome110"}})
            response.raise_for_status()
        return response.text
