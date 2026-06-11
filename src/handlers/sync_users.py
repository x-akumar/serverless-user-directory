import json

from src.services.external_api_service import fetch_users
from src.services.dynamodb_service import save_user


def lambda_handler(event, context):

    users = fetch_users()

    users_processed = 0

    for user in users:

        save_user(user)

        users_processed += 1

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "users synced successfull",
            "usersProcessed": users_processed
        })
    }