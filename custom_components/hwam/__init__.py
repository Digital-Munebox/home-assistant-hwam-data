from homeassistant.core import HomeAssistant

from .const import DOMAIN

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the HWAM integration."""
    hass.data[DOMAIN] = {}
    return True
