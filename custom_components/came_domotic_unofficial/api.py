"""CAME Domotic Unofficial API Client."""
from __future__ import annotations

import asyncio
import logging
import socket
from typing import Any

import aiohttp

TIMEOUT = 10

_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json; charset=UTF-8"}


class CameDomoticUnofficialApiClientError(Exception):
    """Base exception for API client errors."""


class CameDomoticUnofficialApiClientCommunicationError(
    CameDomoticUnofficialApiClientError
):
    """Exception for communication errors."""


class CameDomoticUnofficialApiClientAuthenticationError(
    CameDomoticUnofficialApiClientError
):
    """Exception for authentication errors."""


def _verify_response_or_raise(response: aiohttp.ClientResponse) -> None:
    """Verify that the response is valid."""
    if response.status in (401, 403):
        msg = "Invalid credentials"
        raise CameDomoticUnofficialApiClientAuthenticationError(msg)
    response.raise_for_status()


class CameDomoticUnofficialApiClient:
    """CAME Domotic Unofficial API Client."""

    def __init__(
        self, username: str, password: str, session: aiohttp.ClientSession
    ) -> None:
        """Initialize the API client."""
        self._username = username
        self._password = password
        self._session = session

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        return await self._api_wrapper("get", url)

    async def async_set_title(self, value: str) -> Any:
        """Set title via the API."""
        url = "https://jsonplaceholder.typicode.com/posts/1"
        return await self._api_wrapper(
            "patch", url, data={"title": value}, headers=HEADERS
        )

    async def _api_wrapper(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        headers: dict | None = None,
    ) -> Any:
        """Get information from the API."""
        try:
            async with asyncio.timeout(TIMEOUT):
                response = await self._session.request(
                    method=method,
                    url=url,
                    headers=headers or {},
                    json=data,
                )
                _verify_response_or_raise(response)
                return await response.json()

        except TimeoutError as exception:
            raise CameDomoticUnofficialApiClientCommunicationError(
                f"Timeout error fetching information from {url}"
            ) from exception

        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise CameDomoticUnofficialApiClientCommunicationError(
                f"Error fetching information from {url}"
            ) from exception

        except CameDomoticUnofficialApiClientAuthenticationError:
            raise

        except Exception as exception:
            raise CameDomoticUnofficialApiClientError(
                f"Error parsing information from {url}"
            ) from exception
