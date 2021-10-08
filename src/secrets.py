import os
from logging import Logger

import yaml

from src.logger import logger


SECRETS_PATH = f"{os.environ['ARGUS_DIRECTORY']}/secrets.yaml"


def get_secrets(path: str = SECRETS_PATH, logger: Logger = logger) -> dict:
    logger.debug(f"Getting secrets from {path}")
    with open(path, "r") as fh:
        secrets = yaml.safe_load(fh)
    return secrets


secrets = get_secrets()
