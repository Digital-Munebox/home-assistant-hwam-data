from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class HWAMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HWAM."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            # Validate the IP address
            ip_address = user_input["host"]
            if not self._is_valid_ip(ip_address):
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_form_schema(),
                    errors={"host": "invalid_host"}
                )

            # Save configuration and exit
            return self.async_create_entry(title="HWAM Stove", data=user_input)

        # Show the configuration form
        return self.async_show_form(
            step_id="user",
            data_schema=self._get_form_schema()
        )

    def _get_form_schema(self):
        """Define the form schema."""
        from homeassistant.helpers import config_validation as cv
        import voluptuous as vol
        return vol.Schema({
            vol.Required("host"): cv.string,
        })

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return HWAMOptionsFlowHandler(config_entry)

    def _is_valid_ip(self, ip):
        """Validate an IP address."""
        from ipaddress import ip_address
        try:
            ip_address(ip)
            return True
        except ValueError:
            return False


class HWAMOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for HWAM."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # No additional options yet, return empty form
        return self.async_show_form(step_id="init", data_schema=vol.Schema({}))
