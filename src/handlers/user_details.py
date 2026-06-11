import json
from decimal import Decimal

from src.services.dynamodb_service import get_user_by_id


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):

    user_id = int(event["pathParameters"]["id"])

    user = get_user_by_id(user_id)

    if not user:

        return {
            "statusCode": 404,
            "body": json.dumps({
                "error": "User not found"
            })
        }

    return {
        "statusCode": 200,
        "body": json.dumps(user, cls=DecimalEncoder)
    }