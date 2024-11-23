"""HWAM API Client."""
import asyncio
import aiohttp
import async_timeout
import logging
import json
from typing import Dict, Optional

_LOGGER = logging.getLogger(__name__)

REQUIRED_KEYS = {
    "operation_mode",
    "stove_temperature",
    "room_temperature",
    "oxygen_level"
}

VALID_CONTENT_TYPES = {
    'application/json',
    'text/json',
    'text/plain'
}

class HWAMApi:
    """HWAM API Client."""

    def __init__(self, host: str, session: Optional[aiohttp.ClientSession] = None):
        """Initialize the API client."""
        self._host = host
        self._session = session or aiohttp.ClientSession()
        self._base_url = f"http://{host}"
        _LOGGER.debug("Initialized HWAM API client with base URL: %s", self._base_url)

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        url = f"{self._base_url}/get_stove_data"
        _LOGGER.debug("Fetching data from: %s", url)

        try:
            async with async_timeout.timeout(15):  # Augmenté à 15 secondes
                async with self._session.get(url) as response:
                    _LOGGER.debug("Response status: %s", response.status)
                    content_type = response.headers.get('Content-Type', '').lower().split(';')[0]
                    _LOGGER.debug("Response content type: %s", content_type)

                    if response.status == 200:
                        try:
                            text_response = await response.text()
                            data = json.loads(text_response)
                            if all(key in data for key in REQUIRED_KEYS):
                                _LOGGER.debug("Successfully parsed and validated data")
                                return data
                            else:
                                missing_keys = REQUIRED_KEYS - set(data.keys())
                                _LOGGER.error("Missing required keys: %s", missing_keys)
                        except json.JSONDecodeError as err:
                            _LOGGER.error("Failed to parse JSON: %s", err)
                    else:
                        _LOGGER.error("Failed to get data. Status: %s", response.status)
                    return {}
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while connecting to %s", url)
            raise
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error: %s", err)
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error: %s", err, exc_info=True)
            raise

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the HWAM stove."""
        try:
            _LOGGER.debug("Validating connection to HWAM stove at %s", self._host)
            data = await self.async_get_data()
            return all(key in data for key in REQUIRED_KEYS)
        except Exception as err:
            _LOGGER.error("Validation failed: %s", err)
            return False

    async def close(self):
        """Avoid explicit session closure; managed by Home Assistant."""
        if self._session and not self._session.closed:
            _LOGGER.debug("Session is still open. Leaving it to Home Assistant.")
