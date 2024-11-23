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
        _LOGGER.debug("Initialized HWAM API client with base URL: %s", self._base_url)

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        url = f"{self._base_url}/get_stove_data"
        _LOGGER.debug("Attempting to fetch data from: %s", url)
        
        try:
            async with async_timeout.timeout(10):
                async with self._session.get(url) as response:
                    _LOGGER.debug("Response status: %s", response.status)
                    if response.status == 200:
                        data = await response.json()
                        _LOGGER.debug("Received data: %s", data)
                        return data
                    
                    # Log the response content in case of error
                    error_text = await response.text()
                    _LOGGER.error("Failed to get data. Status: %s, Response: %s", 
                                response.status, error_text)
                    return {}
                    
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while connecting to %s", url)
            raise
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error while connecting to %s: %s", url, str(err))
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error while getting data from %s: %s", 
                         url, str(err), exc_info=True)
            raise

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the HWAM stove."""
        try:
            _LOGGER.debug("Validating connection to HWAM stove at %s", self._host)
            data = await self.async_get_data()
            is_valid = bool(data)
            _LOGGER.debug("Connection validation result: %s", 
                         "Success" if is_valid else "Failed (empty data)")
            return is_valid
        except Exception as err:
            _LOGGER.error("Connection validation failed with error: %s", str(err))
            return False

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
