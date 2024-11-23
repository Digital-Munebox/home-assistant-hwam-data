HWAM Data Integration for Home Assistant

This integration allows you to connect HWAM wood stoves to Home Assistant, enabling monitoring of various parameters like temperature, oxygen level, mode, and more. It also includes binary sensors for specific states like door status.

Features

Sensors

stove_temperature	Stove Temperature	°C	Temperature of the stove, divided by 100 for consistency.
room_temperature	Room Temperature	°C	Ambient temperature in the room, divided by 100 for consistency.
oxygen_level	Oxygen Level	%	Oxygen level measured inside the stove.
valve1_position	Valve 1 Position	%	Position of valve 1 (0-100%).
valve2_position	Valve 2 Position	%	Position of valve 2 (0-100%).
valve3_position	Valve 3 Position	%	Position of valve 3 (0-100%).
maintenance_alarms	Maintenance Alarms	None	Indicates if there are maintenance alarms.
safety_alarms	Safety Alarms	None	Indicates if there are safety alarms.
refill_alarm	Refill Alarm	None	Indicates if a refill is required.
operation_mode	Stove Mode	None	Indicates the current mode of the stove (e.g., "On", "Off").



Binary Sensors

door_open	Door Open	Indicates if the stove door is currently open.
