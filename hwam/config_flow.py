from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN, CONF_IP_ADDRESS

@config_entries.HANDLERS.register(DOMAIN)
class HWAMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """HWAM configuration flow."""

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="HWAM Stove", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required(CONF_IP_ADDRESS): str}),
        )
