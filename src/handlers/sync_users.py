import json

from src.services.external_api_service import fetch_users
from src.services.dynamodb_service import save_user
from src.utils.logger import get_logger

logger = get_logger(__name__)


def lambda_handler(event, context):
    logger.info("Starting user sync")

    users = fetch_users()
    users_processed = 0

    for user in users:
        save_user(user)
        users_processed += 1

    logger.info("Sync complete", extra={"usersProcessed": users_processed})

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Users synced successfully",
            "usersProcessed": users_processed
        })
    }
