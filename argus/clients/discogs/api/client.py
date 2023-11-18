from dataclasses import dataclass, field
from json import JSONDecodeError
from logging import Logger
from typing import Optional

from discogs_client.client import Client
from discogs_client.models import User, Wantlist, Release, List
from retry import retry

from argus.logger import logger


@dataclass
class DiscogsApiClient:
    token: str
    client: Client = field(init=False)
    _identity: Optional[User] = None
    logger: Logger = logger

    def __post_init__(self) -> None:
        self.client = Client(user_agent="Argus", user_token=self.token)

    def identity(self) -> User:
        if not self._identity:
            self._identity = self.client.identity()
        return self._identity

    @property
    def wantlist(self) -> Wantlist:
        return self.identity().wantlist

    def release(self, release_id: int) -> Release:
        return self.client.release(release_id)

    def list(self, list_id: int) -> List:
        return self.client.list(list_id)

    @retry(
        exceptions=JSONDecodeError,  # user.wantlist can raise JSONDecodeError
        delay=1,
        tries=3,
        backoff=2,
    )
    def get_wantlist_ids(self, page_size: int = 100, pages: int = 1) -> list:
        """
        Returns the IDs in the wantlist for the account linked to the token.

        By default, retrieves 1 page of 100 items.
        """
        self.logger.info("Getting wantlist")
        self.wantlist.per_page = page_size
        wantlist_ids = []
        for page_number in range(pages):
            wantlist_ids += [str(item.id) for item in self.wantlist.page(page_number)]
        self.logger.info(f"Found {len(wantlist_ids)} releases in wantlist")
        return wantlist_ids
