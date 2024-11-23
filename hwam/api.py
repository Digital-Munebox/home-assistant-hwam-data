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

    async def _make_request(self, endpoint: str) -> Dict:
        """Make a request to the HWAM API."""
        url = f"{self._base_url}/{endpoint}"
        _LOGGER.debug("Making request to: %s", url)
        
        try:
            async with async_timeout.timeout(10):
                async with self._session.get(url) as response:
                    _LOGGER.debug("Response status: %s", response.status)
                    content_type = response.headers.get('Content-Type', '')
                    _LOGGER.debug("Response content type: %s", content_type)
                    
                    # Log raw response
                    response_text = await response.text()
                    _LOGGER.debug("Raw response: %s", response_text)
                    
                    if response.status == 200:
                        if 'application/json' in content_type:
                            return await response.json()
                        else:
                            _LOGGER.error("Expected JSON response but got content type: %s", content_type)
                            return {}
                    
                    _LOGGER.error("Request failed with status %s: %s", response.status, response_text)
                    return {}
                    
        except asyncio.TimeoutError:
            _LOGGER.error("Timeout while connecting to %s", url)
            raise
        except aiohttp.ClientError as err:
            _LOGGER.error("Network error while connecting to %s: %s", url, str(err))
            raise
        except Exception as err:
            _LOGGER.error("Unexpected error while getting data from %s: %s", url, str(err), exc_info=True)
            raise

    async def async_get_data(self) -> Dict:
        """Get data from the HWAM stove."""
        # Try different potential endpoints
        endpoints = ['get_stove_data', 'data', 'status', 'api/status']
        
        for endpoint in endpoints:
            try:
                _LOGGER.debug("Trying endpoint: %s", endpoint)
                data = await self._make_request(endpoint)
                if data:
                    _LOGGER.debug("Successfully got data from endpoint: %s", endpoint)
                    return data
            except Exception as err:
                _LOGGER.debug("Failed to get data from endpoint %s: %s", endpoint, err)
                continue
        
        _LOGGER.error("Failed to get data from any endpoint")
        return {}

    async def async_validate_connection(self) -> bool:
        """Validate the connection to the HWAM stove."""
        try:
            _LOGGER.debug("Validating connection to HWAM stove at %s", self._host)
            data = await self.async_get_data()
            is_valid = bool(data)
            _LOGGER.debug("Connection validation result: %s (Data: %s)", 
                         "Success" if is_valid else "Failed (empty data)",
                         str(data)[:200] if data else "No data")
            return is_valid
        except Exception as err:
            _LOGGER.error("Connection validation failed with error: %s", str(err))
            return False

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
