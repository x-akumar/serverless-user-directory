import requests

from src.services.secrets_service import get_secrets


def fetch_users():

    secrets = get_secrets()

    base_url = secrets["API_BASE_URL"]

    api_key = secrets["API_KEY"]

    api_username = secrets["API_USERNAME"]

    api_password = secrets["API_PASSWORD"]

    headers = {
        "x-api-key": api_key
    }

    try:

        response = requests.get(
            base_url,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data["users"]

    except requests.exceptions.RequestException as error:

        print(f"External API error: {error}")

        raise Exception("Unable to retrieve users")