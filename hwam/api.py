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
        _LOGGER.debug("Initialized HWAM API client for host: %s", host)

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        endpoints = [
            "/api/v1/status",
            "/api/status",
            "/api/data",
            "/status",
            "/data",
            "/"
        ]

        for endpoint in endpoints:
            url = f"{self._base_url}{endpoint}"
            _LOGGER.debug("Trying endpoint: %s", url)
            
            try:
                async with async_timeout.timeout(5):  # Reduced timeout to 5 seconds
                    _LOGGER.debug("Making GET request to: %s", url)
                    async with self._session.get(url) as response:
                        _LOGGER.debug("Response status from %s: %s", url, response.status)
                        
                        if response.status == 200:
                            try:
                                data = await response.json()
                                _LOGGER.debug("Received data from %s: %s", url, data)
                                if data:  # If we got any data
                                    return data
                            except Exception as err:
                                _LOGGER.debug("Error parsing JSON from %s: %s", url, err)
                                # Try to read raw text
                                text = await response.text()
                                _LOGGER.debug("Raw response: %s", text)
                        else:
                            text = await response.text()
                            _LOGGER.debug("Non-200 response text: %s", text)
                            
            except asyncio.TimeoutError:
                _LOGGER.debug("Timeout reaching %s", url)
            except aiohttp.ClientError as err:
                _LOGGER.debug("Network error reaching %s: %s", url, str(err))
            except Exception as err:
                _LOGGER.debug("Unexpected error trying %s: %s", url, str(err))

        _LOGGER.error("Failed to get data from HWAM stove at %s after trying all endpoints", self._host)
        return {}

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the HWAM stove."""
        _LOGGER.debug("Starting connection validation for %s", self._host)
        try:
            # First try a simple TCP connection
            _, writer = await asyncio.open_connection(self._host, 80)
            writer.close()
            await writer.wait_closed()
            _LOGGER.debug("TCP connection successful")

            # Then try to get data
            data = await self.async_get_data()
            _LOGGER.debug("Data retrieval result: %s", bool(data))
            return bool(data)
        except Exception as err:
            _LOGGER.error("Connection validation failed: %s", err)
            return False

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
