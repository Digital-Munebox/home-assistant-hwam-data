from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up HWAM sensors based on a config entry."""
    sensors = [
        HWAMSensor(hass, config_entry, "stove_temperature", "Stove Temperature", "°C"),
        HWAMSensor(hass, config_entry, "room_temperature", "Room Temperature", "°C"),
        HWAMSensor(hass, config_entry, "oxygen_level", "Oxygen Level", "%"),
        HWAMSensor(hass, config_entry, "valve1_position", "Valve 1 Position", "%"),
        HWAMSensor(hass, config_entry, "valve2_position", "Valve 2 Position", "%"),
        HWAMSensor(hass, config_entry, "valve3_position", "Valve 3 Position", "%"),
        HWAMSensor(hass, config_entry, "maintenance_alarms", "Maintenance Alarms"),
        HWAMSensor(hass, config_entry, "safety_alarms", "Safety Alarms"),
        HWAMSensor(hass, config_entry, "refill_alarm", "Refill Alarm"),
        HWAMBinarySensor(hass, config_entry, "door_open", "Door Open"),
        HWAMModeSensor(hass, config_entry, "operation_mode", "Stove Mode"),
    ]
    async_add_entities(sensors, update_before_add=True)


class HWAMSensor(SensorEntity):
    """Representation of a HWAM sensor."""

    def __init__(self, hass, config_entry, key, name, unit=None):
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
        raw_data = self.hass.data[DOMAIN].get(self._key, None)
        if self._key in ["stove_temperature", "room_temperature"] and raw_data is not None:
            self._state = round(raw_data / 100, 2)  # Conversion pour les températures
        else:
            self._state = raw_data


class HWAMBinarySensor(SensorEntity):
    """Representation of a binary sensor for HWAM."""

    def __init__(self, hass, config_entry, key, name):
        """Initialize the HWAM binary sensor."""
        self.hass = hass
        self.config_entry = config_entry
        self._key = key
        self._name = name
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the binary sensor."""
        return self._state

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the binary sensor."""
        raw_data = self.hass.data[DOMAIN].get(self._key, None)
        self._state = bool(raw_data)


class HWAMModeSensor(SensorEntity):
    """Representation of the stove mode based on operation_mode."""

    def __init__(self, hass, config_entry, key, name):
        """Initialize the HWAM mode sensor."""
        self.hass = hass
        self.config_entry = config_entry
        self._key = key
        self._name = name
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the mode sensor."""
        raw_mode = self.hass.data[DOMAIN].get(self._key, None)
        mode_map = {
            2: "Éteint",
            9: "Allumé"
        }
        self._state = mode_map.get(raw_mode, "Inconnu")
