from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HWAM sensors based on a config entry."""
    sensors = [
        HWAMSensor(hass, config_entry, "stove_temperature", "Stove Temperature", "°C"),
        HWAMSensor(hass, config_entry, "room_temperature", "Room Temperature", "°C"),
    ]
    async_add_entities(sensors, update_before_add=True)


class HWAMSensor(SensorEntity):
    """Representation of a HWAM sensor."""

    def __init__(self, hass, config_entry, key, name, unit):
        """Initialize the HWAM sensor."""
        self.hass = hass
        self.config_entry = config_entry
        self._key = key
        self._name = name
        self._unit = unit
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    async def async_update(self):
        """Fetch new state data for the sensor."""
        # Simuler une récupération des données pour le moment
        self._state = self.hass.data[DOMAIN].get(self._key, None)
