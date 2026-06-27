import json

from src.services.dynamodb_service import get_all_users
from src.utils.json_utils import DecimalEncoder


def lambda_handler(event, context):
    users = get_all_users()

    return {
        "statusCode": 200,
        "body": json.dumps(users, cls=DecimalEncoder)
    }
