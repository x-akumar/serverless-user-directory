import json

from src.services.dynamodb_service import search_users
from src.utils.json_utils import DecimalEncoder

ALLOWED_SEARCH_KEYS = {"username", "email", "firstName", "lastName"}


def lambda_handler(event, context):
    query_params = event.get("queryStringParameters")

    if not query_params:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing query parameters"})
        }

    search_key = list(query_params.keys())[0]

    if search_key not in ALLOWED_SEARCH_KEYS:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": f"Invalid search field. Allowed: {', '.join(sorted(ALLOWED_SEARCH_KEYS))}"
            })
        }

    search_value = query_params[search_key]

    users = search_users(search_key, search_value)

    return {
        "statusCode": 200,
        "body": json.dumps(users, cls=DecimalEncoder)
    }
