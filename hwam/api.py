"""HWAM API Client."""
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
        self._base_url = f"http://{host}/api"

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        try:
            async with async_timeout.timeout(10):
                async with self._session.get(f"{self._base_url}/status") as response:
                    if response.status != 200:
                        _LOGGER.error("Failed to get data from HWAM stove: %s", response.status)
                        return {}
                    return await response.json()
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Error getting data from HWAM stove: %s", err)
            return {}

    async def async_set_mode(self, mode: int) -> bool:
        """Set operation mode."""
        try:
            async with async_timeout.timeout(10):
                async with self._session.post(
                    f"{self._base_url}/mode",
                    json={"mode": mode}
                ) as response:
                    return response.status == 200
        except (aiohttp.ClientError, asyncio.TimeoutError) as err:
            _LOGGER.error("Error setting mode on HWAM stove: %s", err)
            return False

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
