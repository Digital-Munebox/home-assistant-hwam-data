"""Support for HWAM sensors."""
from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature, PERCENTAGE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "stove_temperature": {
        "name": "Température du poêle",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
        "divide_by": 100,
    },
    "room_temperature": {
        "name": "Température ambiante",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:home-thermometer",
        "divide_by": 100,
    },
    "oxygen_level": {
        "name": "Niveau d'oxygène",
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": PERCENTAGE,
        "icon": "mdi:gas-cylinder",
        "divide_by": 100,
    },
}

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up HWAM sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    async_add_entities(
        HWAMSensor(coordinator, sensor_key, config, entry)
        for sensor_key, config in SENSORS.items()
    )

class HWAMSensor(CoordinatorEntity, SensorEntity):
    """Representation of a HWAM sensor."""

    def __init__(self, coordinator, sensor_key: str, config: dict, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_key = sensor_key
        self._config = config
        self._attr_name = config["name"]
        self._attr_unique_id = f"{entry.entry_id}_{sensor_key}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "HWAM Stove",
            "manufacturer": "HWAM",
        }
        self._attr_device_class = config.get("device_class")
        self._attr_state_class = config.get("state_class")
        self._attr_native_unit_of_measurement = config.get("unit")
        self._attr_icon = config.get("icon")

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        value = self.coordinator.data.get(self._sensor_key)
        if value is None:
            return None
        if "divide_by" in self._config:
            try:
                return round(float(value) / self._config["divide_by"], 1)
            except (ValueError, TypeError):
                return None
        return value
