# conftest.py
import os

import pytest
from dotenv import load_dotenv

from castlabs import ContentPlatform


@pytest.fixture(scope="session", autouse=True)
def load_env():
    """Load environment variables from .env file."""
    load_dotenv()


@pytest.fixture(scope="session", name="platform")
def fixture_platform():
    """Create a ContentPlatform instance."""

    return ContentPlatform(
        organization_urn=os.environ["ORGANIZATION_URN"],
        user_urn=os.environ["USER_URN"],
        api_access_key_id=os.environ["API_ACCESS_KEY_ID"],
        api_secret_access_key=os.environ["API_SECRET_ACCESS_KEY"],
    )
