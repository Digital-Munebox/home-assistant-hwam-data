"""Config flow for HWAM integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import logging

from .api import HWAMApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class HWAMConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for HWAM."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            api = HWAMApi(user_input[CONF_HOST], session)

            try:
                # Test the connection
                if await api.async_validate_connection():
                    await api.close()
                    return self.async_create_entry(
                        title="HWAM Stove",
                        data={CONF_HOST: user_input[CONF_HOST]}
                    )
                errors["base"] = "cannot_connect"
            except Exception as err:  # pylint: disable=broad-except
                _LOGGER.error("Unexpected error occurred: %s", err)
                errors["base"] = "unknown"
            finally:
                await api.close()

        # Show the configuration form
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST): str,
            }),
            errors=errors
        )

    async def async_step_import(self, user_input=None):
        """Handle import from configuration.yaml."""
        return await self.async_step_user(user_input)
