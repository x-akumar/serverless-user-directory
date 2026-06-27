import boto3
import pytest
from moto import mock_aws
from unittest.mock import patch

SAMPLE_USER = {
    "id": 1, "username": "jdoe", "email": "j@example.com",
    "firstName": "John", "lastName": "Doe"
}


@pytest.fixture(autouse=True)
def aws_env(monkeypatch):
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    monkeypatch.setenv("AWS_SECURITY_TOKEN", "testing")
    monkeypatch.setenv("AWS_SESSION_TOKEN", "testing")


@pytest.fixture
def mock_table():
    with mock_aws():
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="users-table",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "N"}],
            BillingMode="PAY_PER_REQUEST"
        )
        yield table


def test_save_and_retrieve_user(mock_table):
    with patch("src.services.dynamodb_service.table", mock_table):
        from src.services.dynamodb_service import save_user, get_user_by_id
        save_user(SAMPLE_USER)
        result = get_user_by_id(1)
        assert result["username"] == "jdoe"
        assert result["email"] == "j@example.com"


def test_get_user_not_found(mock_table):
    with patch("src.services.dynamodb_service.table", mock_table):
        from src.services.dynamodb_service import get_user_by_id
        assert get_user_by_id(999) is None


def test_get_all_users_returns_all(mock_table):
    with patch("src.services.dynamodb_service.table", mock_table):
        from src.services.dynamodb_service import save_user, get_all_users
        save_user(SAMPLE_USER)
        save_user({**SAMPLE_USER, "id": 2, "username": "jsmith"})
        result = get_all_users()
        assert len(result) == 2


def test_search_users_filters_correctly(mock_table):
    with patch("src.services.dynamodb_service.table", mock_table):
        from src.services.dynamodb_service import save_user, search_users
        save_user(SAMPLE_USER)
        save_user({**SAMPLE_USER, "id": 2, "username": "jsmith"})
        result = search_users("username", "jdoe")
        assert len(result) == 1
        assert result[0]["username"] == "jdoe"


def test_search_users_case_insensitive(mock_table):
    with patch("src.services.dynamodb_service.table", mock_table):
        from src.services.dynamodb_service import save_user, search_users
        save_user(SAMPLE_USER)
        result = search_users("username", "JDOE")
        assert len(result) == 1
