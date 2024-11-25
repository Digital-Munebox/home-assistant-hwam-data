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
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "stove_temperature": {
        "name": "Température du poêle",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:thermometer",
    },
    "room_temperature": {
        "name": "Température ambiante",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,
        "icon": "mdi:home-thermometer",
    },
    "oxygen_level": {
        "name": "Niveau d'oxygène",
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": PERCENTAGE,
        "icon": "mdi:gas-cylinder",
    },
    "burn_level": {
        "name": "Niveau de combustion",
        "icon": "mdi:fire",
    },
    "operation_mode": {
        "name": "Mode de fonctionnement",
        "icon": "mdi:cog",
        "value_map": {
            2: "Éteint",
            9: "En marche",
        },
    },
    "phase": {
        "name": "Phase de combustion",
        "icon": "mdi:fire-alert",
        "value_map": {
            1: "Allumage",
            3: "Combustion",
            4: "Brasier",
            5: "Repos",
        },
    },
    "maintenance_alarms": {
        "name": "Alarmes de maintenance",
        "icon": "mdi:alert",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "safety_alarms": {
        "name": "Alarmes de sécurité",
        "icon": "mdi:alert-circle",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "refill_alarm": {
        "name": "Alarme de rechargement",
        "icon": "mdi:bell",
        "device_class": SensorDeviceClass.ENUM,
        "options": ["Aucun", "Rechargement nécessaire"],
        "value_map": {
            False: "Aucun",
            True: "Rechargement nécessaire",
        },
    },
    "door_open": {
        "name": "Porte ouverte",
        "icon": "mdi:door",
        "device_class": SensorDeviceClass.ENUM,
        "options": ["Fermée", "Ouverte"],
        "value_map": {
            False: "Fermée",
            True: "Ouverte",
        },
    },
    "version": {
        "name": "Version du firmware",
        "icon": "mdi:update",
    },
    "wifi_version": {
        "name": "Version du module WiFi",
        "icon": "mdi:wifi",
    },
    "new_fire_wood_time": {
        "name": "Temps avant rechargement",
        "icon": "mdi:timer-sand",
    },
    "service_date": {
        "name": "Date de maintenance",
        "icon": "mdi:calendar-check",
        "device_class": SensorDeviceClass.DATE,
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up HWAM sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    sensors = [
        HWAMSensor(coordinator, sensor_key, config, entry)
        for sensor_key, config in SENSORS.items()
    ]

    async_add_entities(sensors)


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
        stove_data = self.coordinator.data  # Instance de StoveData
        value = getattr(stove_data, self._sensor_key, None)

        if value is None:
            return None

        # Apply value mapping if specified
        if "value_map" in self._config:
            return self._config["value_map"].get(value, value)

        return value

    @property
    def options(self):
        """Return options for ENUM sensors."""
        return self._config.get("options")
