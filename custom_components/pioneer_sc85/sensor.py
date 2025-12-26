from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from .const import AUDIO_FORMATS, get_device_info

async def async_setup_entry(hass, entry, async_add_entities):
    telnet = hass.data["pioneer_sc85"][entry.entry_id]
    async_add_entities([
        AudioFormatSensor(telnet, entry),
        FrontPanelSensor(telnet, entry)
    ])

class AudioFormatSensor(SensorEntity):
    def __init__(self, telnet, entry):
        self.telnet = telnet
        self.entry = entry
        self._state = None
        telnet.register(self._parse)

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.entry)

    @property
    def name(self):
        return "Pioneer Audio Format"

    @property
    def state(self):
        return self._state

    def _parse(self, msg):
        if msg.startswith("AST"):
            self._state = AUDIO_FORMATS.get(msg[-2:])
            self.schedule_update_ha_state()

class FrontPanelSensor(SensorEntity):
    def __init__(self, telnet, entry):
        self.telnet = telnet
        self.entry = entry
        self._state = ""
        telnet.register(self._parse)

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.entry)

    @property
    def name(self):
        return "Pioneer Front Panel"

    @property
    def state(self):
        return self._state

    def _parse(self, msg):
        if msg.startswith("FL"):
            self._state = msg[2:]
            self.schedule_update_ha_state()