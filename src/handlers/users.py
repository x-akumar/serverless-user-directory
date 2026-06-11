import json
from decimal import Decimal

from src.services.dynamodb_service import get_all_users


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return super(DecimalEncoder, self).default(obj)


def lambda_handler(event, context):

    users = get_all_users()

    return {
        "statusCode": 200,
        "body": json.dumps(users, cls=DecimalEncoder)
    }