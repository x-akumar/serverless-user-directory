#lambda actually writes into DynamoDB.
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

    response = table.scan()

    return response["Items"]


def get_user_by_id(user_id):

    response = table.get_item(
        Key={
            "id": user_id
        }
    )

    return response.get("Item")


def search_users(search_key, search_value):

    response = table.scan()

    users = response["Items"]

    filtered_users = []

    for user in users:

        if str(user.get(search_key, "")).lower() == search_value.lower():

            filtered_users.append(user)

    return filtered_users