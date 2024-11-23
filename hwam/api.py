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
        self._base_url = f"http://{host}"

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        try:
            async with async_timeout.timeout(10):
                async with self._session.get(f"{self._base_url}/get_stove_data") as response:
                    if response.status == 200:
                        return await response.json()
                    _LOGGER.error("Failed to get data. Status: %s", response.status)
                    return {}
        except Exception as err:
            _LOGGER.error("Error getting data: %s", err)
            return {}

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the HWAM stove."""
        try:
            data = await self.async_get_data()
            return bool(data)
        except Exception as err:
            _LOGGER.error("Connection validation failed: %s", err)
            return False

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
