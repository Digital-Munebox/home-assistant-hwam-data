"""Support for HWAM binary sensors."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up binary sensors for HWAM."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    async_add_entities([
        HWAMBinarySensor(coordinator, "door_open", "Porte ouverte"),
    ])


class HWAMBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a HWAM binary sensor."""

    def __init__(self, coordinator, key, name):
        super().__init__(coordinator)
        self._key = key
        self._name = name
        self._attr_is_on = self.coordinator.data.get(key)

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        """Return True if the binary sensor is on."""
        return self._attr_is_on
