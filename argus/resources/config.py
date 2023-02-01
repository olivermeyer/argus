import os
import json

import boto3


def get_config():
    try:
        client = boto3.client("secretsmanager", "eu-west-1")
        secret = json.loads(client.get_secret_value(SecretId="argus")["SecretString"])
        config = dict()
        config["user"] = os.environ["USER"]
        config["discogs_token"] = secret[os.environ["DISCOGS_TOKEN_KEY"]]
        config["telegram_token"] = secret["telegram_token"]
        config["telegram_chat_id"] = secret[os.environ["TELEGRAM_CHAT_ID_KEY"]]
        config["telegram_chat_id_errors"] = secret["telegram_chat_id_errors"]
        return config
    except KeyError:
        raise EnvironmentError(f"Missing environment variable")


config = get_config()
