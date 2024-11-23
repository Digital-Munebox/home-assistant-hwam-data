"""HWAM API Client."""
import asyncio
import aiohttp
import async_timeout
import logging
from typing import Dict, Optional

_LOGGER = logging.getLogger(__name__)

class HWAMApi:
    """HWAM API Client."""

    def __init__(self, host: str, session: Optional[aiohttp.ClientSession] = None):
        """Initialize the API client."""
        self._host = host
        self._session = session or aiohttp.ClientSession()
        self._base_url = f"http://{host}"  # Removing /api since we don't know the exact endpoint yet

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        endpoints = [
            "/api/status",  # First try with /api/status
            "/status",      # Then try just /status
            "/data",        # Then try /data
        ]

        for endpoint in endpoints:
            try:
                async with async_timeout.timeout(10):
                    async with self._session.get(f"{self._base_url}{endpoint}") as response:
                        if response.status == 200:
                            return await response.json()
                        _LOGGER.debug("Endpoint %s returned status %s", endpoint, response.status)
            except asyncio.TimeoutError:
                _LOGGER.debug("Timeout trying endpoint %s", endpoint)
            except aiohttp.ClientError as err:
                _LOGGER.debug("Error trying endpoint %s: %s", endpoint, err)
            except Exception as err:
                _LOGGER.debug("Unexpected error trying endpoint %s: %s", endpoint, err)

        _LOGGER.error("Failed to get data from HWAM stove at %s", self._host)
        return {}

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the HWAM stove."""
        try:
            data = await self.async_get_data()
            return bool(data)  # Returns True if we got any data
        except Exception as err:
            _LOGGER.error("Connection validation failed: %s", err)
            return False

    async def async_set_mode(self, mode: int) -> bool:
        """Set operation mode."""
        endpoints = [
            "/api/mode",
            "/mode",
            "/control"
        ]

        for endpoint in endpoints:
            try:
                async with async_timeout.timeout(10):
                    async with self._session.post(
                        f"{self._base_url}{endpoint}",
                        json={"mode": mode}
                    ) as response:
                        if response.status == 200:
                            return True
                        _LOGGER.debug("Endpoint %s returned status %s", endpoint, response.status)
            except Exception as err:
                _LOGGER.debug("Error trying endpoint %s: %s", endpoint, err)

        return False

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
