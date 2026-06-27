import json
from unittest.mock import patch
from src.handlers.sync_users import lambda_handler

MOCK_USERS = [
    {"id": 1, "username": "jdoe", "email": "j@example.com", "firstName": "John", "lastName": "Doe"},
    {"id": 2, "username": "jsmith", "email": "js@example.com", "firstName": "Jane", "lastName": "Smith"},
]


@patch("src.handlers.sync_users.save_user")
@patch("src.handlers.sync_users.fetch_users", return_value=MOCK_USERS)
def test_sync_returns_200(mock_fetch, mock_save):
    response = lambda_handler({}, {})
    assert response["statusCode"] == 200


@patch("src.handlers.sync_users.save_user")
@patch("src.handlers.sync_users.fetch_users", return_value=MOCK_USERS)
def test_sync_reports_correct_count(mock_fetch, mock_save):
    response = lambda_handler({}, {})
    body = json.loads(response["body"])
    assert body["usersProcessed"] == len(MOCK_USERS)


@patch("src.handlers.sync_users.save_user")
@patch("src.handlers.sync_users.fetch_users", return_value=MOCK_USERS)
def test_save_called_for_each_user(mock_fetch, mock_save):
    lambda_handler({}, {})
    assert mock_save.call_count == len(MOCK_USERS)
