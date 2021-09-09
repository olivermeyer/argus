import json
from logging import Logger

from src.logger import logger


def read_state(path: str, logger: Logger = logger) -> dict:
    """
    Reads the state from the path.
    """
    logger.debug(f"Reading state from {path}")
    try:
        with open(path, "r") as fh:
            state = json.load(fh)
        logger.debug("State file found")
    except FileNotFoundError:
        logger.debug(f"State file not found; returning empty state")
        state = {}
    return state


def write_state(state: dict, path: str, logger: Logger = logger) -> None:
    """
    Overwrites the contents of the path with the state.
    """
    logger.debug(f"Writing state to {path}")
    with open(path, "w+") as fh:
        json.dump(state, fh)
