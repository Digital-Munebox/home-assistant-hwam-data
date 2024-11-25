"""Constants for the HWAM integration."""
from homeassistant.const import Platform

# Domaine de l'intégration
DOMAIN = "hwam"

# Plateformes supportées par l'intégration
PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]

# Intervalle de mise à jour en secondes
UPDATE_INTERVAL = 15  # Intervalle entre deux mises à jour des données

# Informations sur l'appareil
DEVICE_INFO = {
    "identifiers": {("hwam", "stove")},
    "name": "HWAM Poêle",
    "manufacturer": "HWAM",
    "model": "IHS Smart Control™",
    "sw_version": "3.20.0",  # Cette version peut être mise à jour dynamiquement
}

# Modes d'opération
OPERATION_MODES = {
    2: "Éteint",
    9: "En marche",
}

# Phases de combustion
COMBUSTION_PHASES = {
    1: "Allumage",
    2: "Préparation",
    3: "Combustion",
    4: "Brasier",
    5: "Repos",
}

# Clés JSON importantes attendues depuis l'API
JSON_KEYS = [
    "stove_temperature",
    "room_temperature",
    "oxygen_level",
    "burn_level",
    "operation_mode",
    "phase",
    "maintenance_alarms",
    "safety_alarms",
    "refill_alarm",
    "door_open",
    "service_date",
    "wifi_version",
    "version",
    "new_fire_wood_hours",
    "new_fire_wood_minutes",
]
