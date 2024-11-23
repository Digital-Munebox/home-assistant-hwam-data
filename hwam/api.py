"""HWAM API Client."""
import asyncio
import aiohttp
import async_timeout
import logging
from typing import Dict, Optional

_LOGGER = logging.getLogger(__name__)

# Définition des clés attendues dans la réponse pour validation
REQUIRED_KEYS = {
    "operation_mode",
    "stove_temperature",
    "room_temperature",
    "oxygen_level"
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
            async with async_timeout.timeout(10):
                async with self._session.get(url) as response:
                    _LOGGER.debug("Response status: %s", response.status)
                    
                    if response.status == 200:
                        try:
                            data = await response.json()
                            _LOGGER.debug("Received data: %s", data)
                            
                            # Validation basique des données
                            if isinstance(data, dict):
                                # Vérifie si toutes les clés requises sont présentes
                                if all(key in data for key in REQUIRED_KEYS):
                                    return data
                                else:
                                    missing_keys = REQUIRED_KEYS - set(data.keys())
                                    _LOGGER.error("Missing required keys in response: %s", missing_keys)
                            else:
                                _LOGGER.error("Response is not a dictionary: %s", type(data))
                            
                            return data
                            
                        except ValueError as err:
                            _LOGGER.error("Failed to parse JSON response: %s", err)
                            return {}
                    
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
            
            # Vérifie si les données sont valides
            is_valid = (
                isinstance(data, dict) and
                all(key in data for key in REQUIRED_KEYS)
            )
            
            if is_valid:
                _LOGGER.debug("Connection validation successful")
            else:
                _LOGGER.error("Connection validation failed - invalid data format")
                
            return is_valid
            
        except Exception as err:
            _LOGGER.error("Connection validation failed with error: %s", str(err))
            return False

    async def close(self):
        """Close the session."""
        if self._session:
            await self._session.close()
