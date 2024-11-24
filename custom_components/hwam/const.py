"""Constants for the HWAM integration."""
from homeassistant.const import Platform

DOMAIN = "hwam"
PLATFORMS = [Platform.SENSOR]

# Polling interval
UPDATE_INTERVAL = 15  # seconds

# Device info
DEVICE_INFO = {
    "identifiers": {("hwam", "stove")},
    "name": "HWAM Poêle",
    "manufacturer": "HWAM",
    "model": "IHS Smart Control™",
    "sw_version": "3.20.0",  # This will be updated dynamically
}

# Operation modes
OPERATION_MODES = {
    2: "Éteint",
    9: "En marche",
}
