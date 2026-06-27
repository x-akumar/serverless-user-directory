import json

from src.services.dynamodb_service import get_user_by_id
from src.utils.json_utils import DecimalEncoder


def lambda_handler(event, context):
    try:
        user_id = int(event["pathParameters"]["id"])
    except (ValueError, TypeError):
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid user ID"})
        }

    user = get_user_by_id(user_id)

    if not user:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "User not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(user, cls=DecimalEncoder)
    }
