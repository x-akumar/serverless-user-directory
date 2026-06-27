import json
from unittest.mock import patch
from src.handlers.user_details import lambda_handler

MOCK_USER = {
    "id": 1, "username": "jdoe", "email": "j@example.com",
    "firstName": "John", "lastName": "Doe"
}


def make_event(user_id):
    return {"pathParameters": {"id": str(user_id)}}


@patch("src.handlers.user_details.get_user_by_id", return_value=MOCK_USER)
def test_found_returns_200(mock_fn):
    response = lambda_handler(make_event(1), {})
    assert response["statusCode"] == 200


@patch("src.handlers.user_details.get_user_by_id", return_value=MOCK_USER)
def test_found_returns_user_data(mock_fn):
    response = lambda_handler(make_event(1), {})
    assert json.loads(response["body"]) == MOCK_USER


@patch("src.handlers.user_details.get_user_by_id", return_value=None)
def test_not_found_returns_404(mock_fn):
    response = lambda_handler(make_event(999), {})
    assert response["statusCode"] == 404


def test_non_numeric_id_returns_400():
    response = lambda_handler(make_event("abc"), {})
    assert response["statusCode"] == 400
