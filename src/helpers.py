from src.logger import logger


def get_new_listing_ids(current_ids, old_ids, logger=logger):
    """
    Derives new listings IDs from current and old listings IDs.
    """
    if current_ids:
        new_ids = list(set(current_ids) - set(old_ids))
    else:
        new_ids = []
    logger.info(f"Found {len(new_ids)} new listing IDs")
    return new_ids
