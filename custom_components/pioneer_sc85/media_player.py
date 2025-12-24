from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MediaPlayerState,
    MediaPlayerEntityFeature
)
from .const import INPUTS, ZONES

SUPPORT_FLAGS = (
    MediaPlayerEntityFeature.TURN_ON |
    MediaPlayerEntityFeature.TURN_OFF |
    MediaPlayerEntityFeature.VOLUME_SET |
    MediaPlayerEntityFeature.VOLUME_MUTE |
    MediaPlayerEntityFeature.SELECT_SOURCE
)

async def async_setup_entry(hass, entry, async_add_entities):
    telnet = hass.data["pioneer_sc85"][entry.entry_id]
    entities = [PioneerZone(telnet, name, prefix) for name, prefix in ZONES.items()]
    async_add_entities(entities)

class PioneerZone(MediaPlayerEntity):
    def __init__(self, telnet, zone, prefix):
        self.telnet = telnet
        self.zone = zone
        self.prefix = prefix
        self._state = MediaPlayerState.OFF
        self._volume = 0
        self._muted = False
        self._source = None
        telnet.register(self._parse)

    @property
    def name(self):
        return f"Pioneer SC-85 {self.zone.capitalize()}"

    @property
    def supported_features(self):
        return SUPPORT_FLAGS

    @property
    def state(self):
        return self._state

    @property
    def volume_level(self):
        return self._volume / 160

    @property
    def is_volume_muted(self):
        return self._muted

    @property
    def source(self):
        return self._source

    @property
    def source_list(self):
        return list(INPUTS.values())

    async def async_turn_on(self):
        await self.telnet.send(f"{self.prefix}PO")

    async def async_turn_off(self):
        await self.telnet.send(f"{self.prefix}PF")

    async def async_set_volume_level(self, volume):
        await self.telnet.send(f"{self.prefix}VL{int(volume*160):03d}")

    async def async_mute_volume(self, mute):
        await self.telnet.send(f"{self.prefix}{'MO' if mute else 'MF'}")

    async def async_select_source(self, source):
        for code, name in INPUTS.items():
            if name == source:
                await self.telnet.send(f"{self.prefix}{code}")

    def _parse(self, msg):
        if msg.startswith(f"{self.prefix}PWR"):
            self._state = MediaPlayerState.ON if msg.endswith("1") else MediaPlayerState.OFF
        elif msg.startswith(f"{self.prefix}VOL"):
            self._volume = int(msg[-3:])
        elif msg.startswith(f"{self.prefix}MUT"):
            self._muted = msg.endswith("1")
        elif msg.startswith(f"{self.prefix}FN"):
            self._source = INPUTS.get(msg[:4])
        self.schedule_update_ha_state()
