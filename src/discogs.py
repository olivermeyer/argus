from typing import List

import discogs_client

from src.logger import logger
from src.secrets import secrets


def get_wantlist_ids(
        discogs_token: str = secrets["discogs_token"]
) -> List[str]:
    """
    Returns the IDs in the wantlist for the account linked to the token.
    """
    logger.info("Fetching wantlist")
    discogs = discogs_client.Client(
        user_agent='Argus',
        user_token=discogs_token
    )
    user = discogs.identity()
    wantlist = user.wantlist
    return [str(item.id) for item in wantlist]
