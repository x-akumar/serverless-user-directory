import requests

from src.services.secrets_service import get_secrets
from src.utils.logger import get_logger

logger = get_logger(__name__)


def fetch_users():
    secrets = get_secrets()

    base_url = secrets["API_BASE_URL"]
    api_key = secrets["API_KEY"]

    headers = {"x-api-key": api_key}

    try:
        logger.info(f"Fetching users from external API: {base_url}")
        response = requests.get(base_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Fetched {len(data['users'])} users from external API")
        return data["users"]

    except requests.exceptions.RequestException as error:
        logger.error(f"External API error: {error}")
        raise Exception("Unable to retrieve users")
