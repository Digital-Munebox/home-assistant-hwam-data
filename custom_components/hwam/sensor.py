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
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
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
    "valve1_position": {
        "name": "Position valve 1",
        "unit": PERCENTAGE,
        "icon": "mdi:valve",
    },
    "valve2_position": {
        "name": "Position valve 2",
        "unit": PERCENTAGE,
        "icon": "mdi:valve",
    },
    "valve3_position": {
        "name": "Position valve 3",
        "unit": PERCENTAGE,
        "icon": "mdi:valve",
    },
    "burn_level": {
        "name": "Niveau de combustion",
        "icon": "mdi:fire",
    },
    "combustion_status": {
        "name": "Statut de la combustion",
        "icon": "mdi:fire-alert",
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
        "name": "Phase",
        "icon": "mdi:chart-timeline",
    },
    "refill_alarm": {
        "name": "Alarme de remplissage",
        "icon": "mdi:bell",
        "device_class": SensorDeviceClass.ENUM,
        "options": ["Normal", "Remplir"],
        "value_map": {
            0: "Normal",
            1: "Remplir",
        },
    },
    "maintenance_alarms": {
        "name": "Alarmes maintenance",
        "icon": "mdi:alert",
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "safety_alarms": {
        "name": "Alarmes sécurité",
        "icon": "mdi:alert-circle",
        "entity_category": EntityCategory.DIAGNOSTIC,
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
    "service_date": {
        "name": "Date de maintenance",
        "icon": "mdi:calendar-clock",
        "device_class": SensorDeviceClass.DATE,
        "entity_category": EntityCategory.DIAGNOSTIC,
    },
    "new_fire_wood_hours": {
        "name": "Heures avant rechargement",
        "icon": "mdi:timer-sand",
    },
    "new_fire_wood_minutes": {
        "name": "Minutes avant rechargement",
        "icon": "mdi:timer-sand",
    },
}

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up HWAM sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    # Ajouter les capteurs définis dans SENSORS
    sensors = [
        HWAMSensor(coordinator, sensor_key, config, entry)
        for sensor_key, config in SENSORS.items()
    ]
    
    # Ajouter des capteurs pour les services interactifs
    sensors.append(HWAMCommandSensor(coordinator, "burn_level", entry, "Niveau de combustion"))
    sensors.append(HWAMCommandSensor(coordinator, "combustion_status", entry, "Statut de la combustion"))
    
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
        value = self.coordinator.data.get(self._sensor_key)
        if value is None:
            return None
        if "divide_by" in self._config:
            try:
                return round(float(value) / self._config["divide_by"], 1)
            except (ValueError, TypeError):
                return None
        if "value_map" in self._config:
            return self._config["value_map"].get(value, value)
        return value


class HWAMCommandSensor(CoordinatorEntity, SensorEntity):
    """Representation of a HWAM interactive command sensor."""

    def __init__(self, coordinator, command: str, entry, name: str):
        """Initialize the interactive sensor."""
        super().__init__(coordinator)
        self._command = command
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{command}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "HWAM Stove",
            "manufacturer": "HWAM",
        }

    @property
    def native_value(self):
        """Return the value of the command."""
        return self.coordinator.data.get(self._command)
