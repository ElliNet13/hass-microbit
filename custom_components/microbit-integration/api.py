"""Sample API Client."""

from __future__ import annotations

import socket
from typing import Any

import aiohttp
import async_timeout


class IntegrationBlueprintApiClientError(Exception):
    """Exception to indicate a general API error."""


class IntegrationBlueprintApiClientCommunicationError(
    IntegrationBlueprintApiClientError,
):
    """Exception to indicate a communication error."""


class IntegrationBlueprintApiClientAuthenticationError(
    IntegrationBlueprintApiClientError,
):
    """Exception to indicate an authentication error."""


class IntegrationBlueprintApiClient:
    """Sample API Client."""

    def __init__(
        self,
        serial_port: str,
    ) -> None:
        """Sample API Client."""
        self._serial_port = serial_port

    async def async_get_data(self) -> Any:
        """Get data from the API."""
        return "test data"

    async def async_set_title(self, value: str) -> Any:
        """Get data from the API."""
        return "test title"
