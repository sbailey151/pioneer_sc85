from homeassistant.components.select import SelectEntity
from .const import DSP_MODES

async def async_setup_entry(hass, entry, async_add_entities):
    telnet = hass.data["pioneer_sc85"][entry.entry_id]
    async_add_entities([DSPSelect(telnet)])

class DSPSelect(SelectEntity):
    def __init__(self, telnet):
        self.telnet = telnet
        self._mode = None
        telnet.register(self._parse)

    @property
    def name(self):
        return "Pioneer SC-85 DSP Mode"

    @property
    def options(self):
        return list(DSP_MODES.values())

    @property
    def current_option(self):
        return self._mode

    async def async_select_option(self, option):
        for code, name in DSP_MODES.items():
            if name == option:
                await self.telnet.send(code)

    def _parse(self, msg):
        if msg.endswith("SR"):
            self._mode = DSP_MODES.get(msg)
            self.schedule_update_ha_state()
