# HWAM Integration for Home Assistant

![HWAM Integration] https://github.com/Digital-Munebox/home-assistant-hwam-data.git

## Description

This custom integration allows you to monitor and control your **HWAM Smart Control** wood stove via Home Assistant. It provides real-time data such as:

- Stove temperature
- Room temperature
- Oxygen level
- Burn level
- Maintenance and safety alarms
- Door status

## Features

- Automatic polling of data from your HWAM stove.
- Displays important metrics directly in your Home Assistant dashboard.
- Customizable sensors with unique IDs for seamless integration.
- Local-only communication for enhanced security.

## Installation

### Via HACS

1. Ensure you have [HACS](https://hacs.xyz/) installed in Home Assistant.
2. Add this repository to HACS:
   - Go to **HACS > Integrations > Add Custom Repository**.
   - Enter the repository URL and select **Integration**.
3. Search for **HWAM Integration** in HACS and install it.
4. Restart Home Assistant.

### Manual Installation

1. Download the integration from the repository.
2. Copy the `custom_components/hwam` folder to the `custom_components` folder in your Home Assistant configuration directory.
3. Restart Home Assistant.

## Configuration

1. Go to **Settings > Devices & Services > Add Integration**.
2. Search for `HWAM` and select it.
3. Enter the IP address of your HWAM stove.
4. The integration will automatically fetch all available sensors.

## Supported Sensors

| Sensor Name           | Description                      | Unit       |
|-----------------------|----------------------------------|------------|
| Stove Temperature     | Current temperature of the stove | °C         |
| Room Temperature      | Current ambient temperature      | °C         |
| Oxygen Level          | Current oxygen level in the room | %          |
| Door Open Status      | Whether the stove door is open   | Open/Closed |
| Burn Level            | Current combustion level         | None       |
| Maintenance Alarms    | Maintenance-related alarms       | Diagnostic |
| Safety Alarms         | Safety-related alarms            | Diagnostic |

## Troubleshooting

- Ensure your HWAM stove is powered on and connected to the network.
- Verify that the correct IP address is used during setup.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to enhance the integration.

## Credits

Developed by Adrien PINAUD. Inspired by the awesome Home Assistant community.
