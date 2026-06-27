import boto3


dynamodb = boto3.resource("dynamodb")

table = dynamodb.Table("users-table")


def save_user(user):
    table.put_item(
        Item={
            "id": user["id"],
            "username": user["username"],
            "email": user["email"],
            "firstName": user["firstName"],
            "lastName": user["lastName"]
        }
    )


def get_all_users():
    items = []
    response = table.scan()

    while True:
        items.extend(response["Items"])
        last_key = response.get("LastEvaluatedKey")
        if not last_key:
            break
        response = table.scan(ExclusiveStartKey=last_key)

    return items


def get_user_by_id(user_id):
    response = table.get_item(Key={"id": user_id})
    return response.get("Item")


def search_users(search_key, search_value):
    items = []
    response = table.scan()

    while True:
        items.extend(response["Items"])
        last_key = response.get("LastEvaluatedKey")
        if not last_key:
            break
        response = table.scan(ExclusiveStartKey=last_key)

    return [
        user for user in items
        if str(user.get(search_key, "")).lower() == search_value.lower()
    ]
