"""Constants for the HWAM integration."""
DOMAIN = "hwam"
DEFAULT_NAME = "HWAM Stove"
UPDATE_INTERVAL = 5  # seconds

# API Response Keys
ATTR_STOVE_TEMP = "stove_temperature"
ATTR_ROOM_TEMP = "room_temperature"
ATTR_OXYGEN = "oxygen_level"
ATTR_VALVE1 = "valve1_position"
ATTR_VALVE2 = "valve2_position"
ATTR_VALVE3 = "valve3_position"
ATTR_DOOR = "door_open"
ATTR_MODE = "operation_mode"
ATTR_REFILL = "refill_alarm"

# Operation Modes
MODE_OFF = 2
MODE_ON = 9

# Mode Mapping
MODE_MAP = {
    MODE_OFF: "Off",
    MODE_ON: "On"
}

DEVICE_INFO = {
    "manufacturer": "HWAM",
    "model": "IHS Smart Control™",
    "via_device": None,
}
