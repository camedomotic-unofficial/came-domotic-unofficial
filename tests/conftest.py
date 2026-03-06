"""Global fixtures for CAME Domotic Unofficial integration."""
from unittest.mock import patch

import pytest

from custom_components.came_domotic_unofficial.api import (
    CameDomoticUnofficialApiClientAuthenticationError,
    CameDomoticUnofficialApiClientCommunicationError,
)

pytest_plugins = "pytest_homeassistant_custom_component"

# API URL used by the placeholder API client
API_URL = "https://jsonplaceholder.typicode.com/posts/1"

# Realistic mock data matching what entities expect from coordinator.data
MOCK_API_DATA = {
    "userId": 1,
    "id": 1,
    "title": "foo",
    "body": "some body text",
}


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for all tests via the plugin fixture."""
    return


@pytest.fixture(name="bypass_get_data")
def bypass_get_data_fixture():
    """Skip calls to get data from API, returning realistic mock data."""
    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        return_value=MOCK_API_DATA,
    ):
        yield


@pytest.fixture(name="error_on_get_data")
def error_get_data_fixture():
    """Simulate communication error when retrieving data from API."""
    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=CameDomoticUnofficialApiClientCommunicationError(
            "Connection error"
        ),
    ):
        yield


@pytest.fixture(name="auth_error_on_get_data")
def auth_error_get_data_fixture():
    """Simulate authentication error when retrieving data from API."""
    with patch(
        "custom_components.came_domotic_unofficial.api."
        "CameDomoticUnofficialApiClient.async_get_data",
        side_effect=CameDomoticUnofficialApiClientAuthenticationError(
            "Invalid credentials"
        ),
    ):
        yield
