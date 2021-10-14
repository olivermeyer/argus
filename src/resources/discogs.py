from json import JSONDecodeError
from logging import Logger
from typing import List

import discogs_client
from retry import retry

from src.resources.logger import logger


# user.wantlist can raise JSONDecodeError
@retry(
    exceptions=JSONDecodeError,
    delay=1,
    tries=3,
    backoff=2,
    logger=logger,
)
def get_wantlist_ids(
        discogs_token: str,
        page_size: int = 100,
        logger: Logger = logger
) -> List[str]:
    """
    Returns the IDs in the wantlist for the account linked to the token.
    """
    logger.info("Fetching wantlist")
    discogs = discogs_client.Client(
        user_agent="Argus",
        user_token=discogs_token
    )
    user = discogs.identity()
    wantlist = user.wantlist
    wantlist.per_page = page_size
    return [str(item.id) for item in wantlist]
