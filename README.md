# Pioneer SC-85 Receiver for Home Assistant

Custom integration to control your Pioneer SC-85 AV receiver via Home Assistant.

## Features
- Media player entity for power, volume, input selection, etc.
- Automatic device creation in HA
- Configurable via UI (config flow)

## Installation
1. Install via HACS: Add custom repository → `https://github.com/sbailey151/pioneer_sc85` → Category: Integration
2. Or manually: Copy `custom_components/pioneer_sc85` to your HA config's `custom_components/` folder
3. Restart Home Assistant
4. Go to Settings → Devices & Services → Add Integration → Search for "Pioneer SC-85"

## Configuration
Provide your receiver's IP address and (optional) port.

## Known Limitations
- Currently only basic control (expandable)
- Uses telnet/HTTP API (adjust as needed)

## Credits
Based on work by sbailey151
