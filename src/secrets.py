import os

import yaml


SECRETS_PATH = f"{os.environ['ARGUS_DIRECTORY']}/secrets.yaml"


def get_secrets(path: str = SECRETS_PATH) -> dict:
    with open(path, "r") as fh:
        secrets = yaml.safe_load(fh)
    return secrets


secrets = get_secrets()
