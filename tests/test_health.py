import json
from src.handlers.health import lambda_handler


def test_returns_200():
    response = lambda_handler({}, {})
    assert response["statusCode"] == 200


def test_returns_healthy_status():
    response = lambda_handler({}, {})
    body = json.loads(response["body"])
    assert body["status"] == "healthy"
