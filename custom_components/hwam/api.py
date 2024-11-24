import asyncio
import aiohttp
import async_timeout
import logging
from typing import Dict, Any

_LOGGER = logging.getLogger(__name__)

class HWAMApi:
    """HWAM API Client."""

    ENDPOINT_GET_STOVE_DATA = "/get_stove_data"
    ENDPOINT_START = "/start"
    ENDPOINT_SET_BURN_LEVEL = "/set_burn_level"

    def __init__(self, host: str, session: aiohttp.ClientSession = None):
        """Initialize the API client."""
        self._host = host
        self._session = session or aiohttp.ClientSession()
        self._base_url = f"http://{host}"

    async def async_get_data(self) -> Dict[str, Any]:
        """Retrieve data from the stove."""
        url = f"{self._base_url}{self.ENDPOINT_GET_STOVE_DATA}"
        _LOGGER.debug("Fetching data from: %s", url)
        try:
            async with async_timeout.timeout(15):
                async with self._session.get(url) as response:
                    response.raise_for_status()
                    return await response.json(content_type="text/json")
        except Exception as err:
            _LOGGER.error("Error fetching data: %s", err)
            raise

    async def start_combustion(self) -> bool:
        """Command the stove to start combustion."""
        url = f"{self._base_url}{self.ENDPOINT_START}"
        try:
            async with self._session.get(url) as response:
                data = await response.json()
                return data.get("response") == "OK"
        except Exception as err:
            _LOGGER.error("Error starting combustion: %s", err)
            return False

    async def set_burn_level(self, level: int) -> bool:
        """Set the burn level of the stove."""
        if level < 0 or level > 5:
            raise ValueError("Burn level must be between 0 and 5")
        url = f"{self._base_url}{self.ENDPOINT_SET_BURN_LEVEL}?level={level}"
        try:
            async with self._session.get(url) as response:
                data = await response.json()
                return data.get("response") == "OK"
        except Exception as err:
            _LOGGER.error("Error setting burn level: %s", err)
            return False

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the HWAM stove."""
        try:
            data = await self.async_get_data()
            if data:
                return True
            return False
        except Exception as err:
            _LOGGER.error("Validation failed: %s", err)
            return False

    async def close(self):
        """Close the session."""
        if self._session and not self._session.closed:
            await self._session.close()
