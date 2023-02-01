import json

import boto3


def get_config(user):
    try:
        client = boto3.client("secretsmanager", "eu-west-1")
        secret = json.loads(client.get_secret_value(SecretId="argus")["SecretString"])
        config = dict()
        config["user"] = user
        config["discogs_token"] = secret[f"discogs_token_{user}"]
        config["telegram_token"] = secret["telegram_token"]
        config["telegram_chat_id"] = secret[f"telegram_chat_id_{user}"]
        config["telegram_chat_id_errors"] = secret["telegram_chat_id_errors"]
        return config
    except KeyError:
        raise EnvironmentError(f"Missing environment variable")
