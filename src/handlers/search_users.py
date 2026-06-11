import json
from decimal import Decimal

from src.services.dynamodb_service import search_users


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):

    query_params = event.get("queryStringParameters")

    if not query_params:

        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": "Invalid request"
            })
        }

    search_key = list(query_params.keys())[0]

    search_value = query_params[search_key]

    users = search_users(search_key, search_value)

    return {
        "statusCode": 200,
        "body": json.dumps(users, cls=DecimalEncoder)
    }