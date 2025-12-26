from homeassistant.components.switch import SwitchEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import get_device_info

async def async_setup_entry(hass, entry, async_add_entities):
    telnet = hass.data["pioneer_sc85"][entry.entry_id]
    async_add_entities([
        HDMIThruSwitch(telnet, entry),
        HDMIAMPSwitch(telnet, entry)
    ])

class HDMIThruSwitch(SwitchEntity):
    def __init__(self, telnet, entry):
        self.telnet = telnet
        self.entry = entry
        self._on = False
        telnet.register(self._parse)

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.entry)

    @property
    def name(self):
        return "Pioneer HDMI Pass Through"

    @property
    def is_on(self):
        return self._on

    async def async_turn_on(self):
        await self.telnet.send("HPO")

    async def async_turn_off(self):
        await self.telnet.send("HPF")

    def _parse(self, msg):
        if msg.startswith("HPT"):
            self._on = msg.endswith("1")
            self.schedule_update_ha_state()

class HDMIAMPSwitch(SwitchEntity):
    def __init__(self, telnet, entry):
        self.telnet = telnet
        self.entry = entry
        self._on = True
        telnet.register(self._parse)  # Assuming it gets updates; if not, remove

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.entry)

    @property
    def name(self):
        return "Pioneer HDMI Audio AMP"

    @property
    def is_on(self):
        return self._on

    async def async_turn_on(self):
        await self.telnet.send("HAO")

    async def async_turn_off(self):
        await self.telnet.send("HAF")

    # If there's a status query (e.g., "HA?"), add parsing here
    def _parse(self, msg):
        pass  # Add if you have status feedback