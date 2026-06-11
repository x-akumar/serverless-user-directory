import json
import boto3


client = boto3.client("secretsmanager")


def get_secrets():

    response = client.get_secret_value(
        SecretId="user-directory-secrets"
    )

    secret = response["SecretString"]

    return json.loads(secret)