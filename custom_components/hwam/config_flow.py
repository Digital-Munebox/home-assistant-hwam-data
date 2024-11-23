from homeassistant import config_entries
from .const import DOMAIN

class HWAMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        # Configuration flow will be implemented here
        pass
