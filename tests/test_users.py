import json
from unittest.mock import patch
from src.handlers.users import lambda_handler

MOCK_USERS = [
    {"id": 1, "username": "jdoe", "email": "j@example.com", "firstName": "John", "lastName": "Doe"}
]


@patch("src.handlers.users.get_all_users", return_value=MOCK_USERS)
def test_returns_200(mock_fn):
    response = lambda_handler({}, {})
    assert response["statusCode"] == 200


@patch("src.handlers.users.get_all_users", return_value=MOCK_USERS)
def test_returns_user_list(mock_fn):
    response = lambda_handler({}, {})
    assert json.loads(response["body"]) == MOCK_USERS


@patch("src.handlers.users.get_all_users", return_value=[])
def test_returns_empty_list_when_no_users(mock_fn):
    response = lambda_handler({}, {})
    assert json.loads(response["body"]) == []
