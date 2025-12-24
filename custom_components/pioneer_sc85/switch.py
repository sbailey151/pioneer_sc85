from homeassistant.components.switch import SwitchEntity

async def async_setup_entry(hass, entry, async_add_entities):
    telnet = hass.data["pioneer_sc85"][entry.entry_id]
    async_add_entities([
        HDMIThruSwitch(telnet),
        HDMIAMPSwitch(telnet)
    ])

class HDMIThruSwitch(SwitchEntity):
    def __init__(self, telnet):
        self.telnet = telnet
        self._on = False
        telnet.register(self._parse)

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
    def __init__(self, telnet):
        self.telnet = telnet
        self._on = True

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
