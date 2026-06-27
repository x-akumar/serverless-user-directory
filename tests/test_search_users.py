import json
from unittest.mock import patch
from src.handlers.search_users import lambda_handler

MOCK_USERS = [
    {"id": 1, "username": "jdoe", "email": "j@example.com", "firstName": "John", "lastName": "Doe"}
]


def make_event(params):
    return {"queryStringParameters": params}


@patch("src.handlers.search_users.search_users", return_value=MOCK_USERS)
def test_valid_search_returns_200(mock_fn):
    response = lambda_handler(make_event({"username": "jdoe"}), {})
    assert response["statusCode"] == 200


@patch("src.handlers.search_users.search_users", return_value=MOCK_USERS)
def test_valid_search_returns_results(mock_fn):
    response = lambda_handler(make_event({"username": "jdoe"}), {})
    assert json.loads(response["body"]) == MOCK_USERS


def test_missing_query_params_returns_400():
    response = lambda_handler({"queryStringParameters": None}, {})
    assert response["statusCode"] == 400


def test_invalid_search_key_returns_400():
    response = lambda_handler(make_event({"internalId": "value"}), {})
    assert response["statusCode"] == 400


@patch("src.handlers.search_users.search_users", return_value=[])
def test_no_matches_returns_empty_list(mock_fn):
    response = lambda_handler(make_event({"email": "nobody@example.com"}), {})
    assert json.loads(response["body"]) == []
