"""Support for HWAM sensors."""
from datetime import datetime
import logging
from typing import Any, Optional

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import (
    UnitOfTemperature,
    PERCENTAGE,
    DEVICE_INFO,  # Correction de Device_INFO en DEVICE_INFO
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN, DEVICE_INFO

_LOGGER = logging.getLogger(__name__)

SENSORS = {
    "stove_temperature": {
        "name": "Température du poêle",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": UnitOfTemperature.CELSIUS,  # Correction de TEMP_CELSIUS
        "icon": "mdi:thermometer",
        "divide_by": 100,
    },
    "room_temperature": {
        "name": "Température ambiante",
        "device_class": SensorDeviceClass.TEMPERATURE,
        "state_class": SensorStateClass.MEASUREMENT,
        "unit": TEMP_CELSIUS,
        "icon": "mdi:home-thermometer",
        "divide_by": 100,
    },
    "oxygen_level": {
        "name": "Niveau d'oxygène",
        "device_class": None,
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


async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities):
    """Set up HWAM sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    
    sensors = []
    for sensor_key, sensor_config in SENSORS.items():
        sensors.append(
            HWAMSensor(
                coordinator,
                sensor_key,
                sensor_config,
                entry
            )
        )
    
    async_add_entities(sensors, True)


class HWAMSensor(CoordinatorEntity, SensorEntity):
    """Representation of a HWAM sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        sensor_key: str,
        sensor_config: dict,
        entry
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        
        self._sensor_key = sensor_key
        self._config = sensor_config
        self._attr_name = sensor_config["name"]
        self._attr_unique_id = f"{entry.entry_id}_{sensor_key}"
        self._attr_device_info = DEVICE_INFO
        
        # Set device class if specified
        if "device_class" in sensor_config:
            self._attr_device_class = sensor_config["device_class"]
        
        # Set state class if specified
        if "state_class" in sensor_config:
            self._attr_state_class = sensor_config["state_class"]
            
        # Set entity category if specified
        if "entity_category" in sensor_config:
            self._attr_entity_category = sensor_config["entity_category"]
        
        # Set unit of measurement if specified
        if "unit" in sensor_config:
            self._attr_native_unit_of_measurement = sensor_config["unit"]
            
        # Set icon if specified
        if "icon" in sensor_config:
            self._attr_icon = sensor_config["icon"]

    @property
    def native_value(self) -> Any:
        """Return the sensor value."""
        value = self.coordinator.data.get(self._sensor_key)
        
        if value is None:
            return None
            
        # Handle special case for service_date
        if self._sensor_key == "service_date":
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except (ValueError, TypeError):
                return None
        
        # Apply value mapping if specified
        if "value_map" in self._config:
            return self._config["value_map"].get(value, value)
            
        # Apply division if specified
        if "divide_by" in self._config:
            try:
                return round(float(value) / self._config["divide_by"], 1)
            except (ValueError, TypeError):
                return None
            
        return value
