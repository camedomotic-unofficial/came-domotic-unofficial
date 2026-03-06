"""Tests for CAME Domotic Unofficial API client."""
import asyncio

import aiohttp
import pytest
from custom_components.came_domotic_unofficial.api import (
    CameDomoticUnofficialApiClient,
    CameDomoticUnofficialApiClientAuthenticationError,
    CameDomoticUnofficialApiClientCommunicationError,
    CameDomoticUnofficialApiClientError,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .conftest import API_URL


async def test_api_get_data(hass, aioclient_mock):
    """Test successful GET request."""
    api = CameDomoticUnofficialApiClient("test", "test", async_get_clientsession(hass))

    aioclient_mock.get(API_URL, json={"test": "test"})
    assert await api.async_get_data() == {"test": "test"}


async def test_api_set_title(hass, aioclient_mock):
    """Test successful PATCH request."""
    api = CameDomoticUnofficialApiClient("test", "test", async_get_clientsession(hass))

    aioclient_mock.patch(API_URL, json={"title": "test"})
    result = await api.async_set_title("test")
    assert result == {"title": "test"}


async def test_api_timeout(hass, aioclient_mock):
    """Test API timeout raises CommunicationError."""
    api = CameDomoticUnofficialApiClient("test", "test", async_get_clientsession(hass))

    aioclient_mock.get(API_URL, exc=asyncio.TimeoutError)
    with pytest.raises(CameDomoticUnofficialApiClientCommunicationError):
        await api.async_get_data()


async def test_api_client_error(hass, aioclient_mock):
    """Test aiohttp.ClientError raises CommunicationError."""
    api = CameDomoticUnofficialApiClient("test", "test", async_get_clientsession(hass))

    aioclient_mock.get(API_URL, exc=aiohttp.ClientError)
    with pytest.raises(CameDomoticUnofficialApiClientCommunicationError):
        await api.async_get_data()


async def test_api_parse_error(hass, aioclient_mock):
    """Test unexpected exception raises ApiClientError."""
    api = CameDomoticUnofficialApiClient("test", "test", async_get_clientsession(hass))

    aioclient_mock.get(API_URL, exc=TypeError)
    with pytest.raises(CameDomoticUnofficialApiClientError):
        await api.async_get_data()


async def test_api_authentication_error_401(hass, aioclient_mock):
    """Test 401 response raises AuthenticationError."""
    api = CameDomoticUnofficialApiClient("test", "test", async_get_clientsession(hass))

    aioclient_mock.get(API_URL, status=401)
    with pytest.raises(CameDomoticUnofficialApiClientAuthenticationError):
        await api.async_get_data()


async def test_api_authentication_error_403(hass, aioclient_mock):
    """Test 403 response raises AuthenticationError."""
    api = CameDomoticUnofficialApiClient("test", "test", async_get_clientsession(hass))

    aioclient_mock.get(API_URL, status=403)
    with pytest.raises(CameDomoticUnofficialApiClientAuthenticationError):
        await api.async_get_data()


async def test_api_set_title_timeout(hass, aioclient_mock):
    """Test async_set_title timeout raises CommunicationError."""
    api = CameDomoticUnofficialApiClient("test", "test", async_get_clientsession(hass))

    aioclient_mock.patch(API_URL, exc=asyncio.TimeoutError)
    with pytest.raises(CameDomoticUnofficialApiClientCommunicationError):
        await api.async_set_title("test")
