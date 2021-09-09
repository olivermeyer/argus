from logging import Logger

from src.logger import logger


def abbreviate_condition(condition: str, logger: Logger = logger) -> str:
    """
    Abbreviates the condition string.

    E.g. 'Very Good+ (VG+)' becomes 'VG+'. 'Generic' becomes 'Gen'.
    """
    logger.debug(f"Abbreviating {condition}")
    if "Generic" in condition:
        short_condition = "Gen"
    else:
        short_condition = condition[
            condition.find("(") + 1:condition.find(")")
        ]
    return short_condition
