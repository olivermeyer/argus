from dataclasses import dataclass
from logging import Logger

from aiohttp import ClientSession, TCPConnector
from aiohttp_retry import RetryClient

from argus.objects import logger


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
        connector = TCPConnector(limit=1)
        async with ClientSession(connector=connector) as session:
            client = RetryClient(client_session=session)
            response = await client.get(**kwargs)
            response.raise_for_status()
            response = await response.text()
        return response
