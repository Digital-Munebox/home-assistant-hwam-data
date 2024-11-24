"""Stove data parsing and structure."""
import dataclasses
import datetime
import logging

_LOGGER = logging.getLogger(__name__)

@dataclasses.dataclass
class StoveData:
    updating: bool
    phase: int
    night_lowering: bool
    new_fire_wood_time: datetime.time
    burn_level: int
    operation_mode: int
    maintenance_alarms: int
    safety_alarms: int
    refill_alarm: bool
    version: str
    wifi_version: str
    room_temperature: int
    stove_temperature: int
    oxygen_level: int
    door_open: bool

def stove_data_of(json: dict) -> StoveData:
    """Convert JSON data into a StoveData object."""
    try:
        return StoveData(
            updating=json.get("updating", 0) == 1,
            phase=json.get("phase", 0),
            night_lowering=json.get("night_lowering", 0) == 1,
            new_fire_wood_time=datetime.time(
                hour=json.get("new_fire_wood_hours", 0),
                minute=json.get("new_fire_wood_minutes", 0)),
            burn_level=json.get("burn_level", 0),
            operation_mode=json.get("operation_mode", 0),
            maintenance_alarms=json.get("maintenance_alarms", 0),
            safety_alarms=json.get("safety_alarms", 0),
            refill_alarm=json.get("refill_alarm", 0) == 1,
            version=f"{json.get('version_major', 0)}.{json.get('version_minor', 0)}.{json.get('version_build', 0)}",
            wifi_version=f"{json.get('wifi_version_major', 0)}.{json.get('wifi_version_minor', 0)}.{json.get('wifi_version_build', 0)}",
            room_temperature=json.get("room_temperature", 0) // 100,
            stove_temperature=json.get("stove_temperature", 0) // 100,
            oxygen_level=json.get("oxygen_level", 0) // 100,
            door_open=json.get("door_open", 0) == 1,
        )
    except Exception as e:
        _LOGGER.error("Error converting stove data: %s", e)
        _LOGGER.debug("Raw JSON data: %s", json)
        raise
