"""Stove data parsing and structure."""
import dataclasses
import datetime

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
    return StoveData(
        updating=json["updating"] == 1,
        phase=json["phase"],
        night_lowering=json["night_lowering"] == 1,
        new_fire_wood_time=datetime.time(
            hour=json["new_fire_wood_hours"],
            minute=json["new_fire_wood_minutes"]),
        burn_level=json["burn_level"],
        operation_mode=json["operation_mode"],
        maintenance_alarms=json["maintenance_alarms"],
        safety_alarms=json["safety_alarms"],
        refill_alarm=json["refill_alarm"] == 1,
        version=f"{json['version_major']}.{json['version_minor']}.{json['version_build']}",
        wifi_version=f"{json['wifi_version_major']}.{json['wifi_version_minor']}.{json['wifi_version_build']}",
        room_temperature=json["room_temperature"] // 100,
        stove_temperature=json["stove_temperature"] // 100,
        oxygen_level=json["oxygen_level"] // 100,
        door_open=json["door_open"] == 1,
    )
