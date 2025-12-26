"""Pioneer SC-85 Media Player integration for Home Assistant."""

from homeassistant.components.media_player import MediaPlayerEntity
from homeassistant.components.media_player.const import (
    MediaPlayerState,
    MediaPlayerEntityFeature,
)
from homeassistant.helpers.device_registry import DeviceInfo
import asyncio
import logging

from .const import (
    INPUTS, get_device_info,
    INPUT_CMD_SUFFIXES, INPUT_PATTERNS, INPUT_QUERY_SUFFIXES,
    MUTE_QUERY_SUFFIXES, MUTE_PATTERNS, MUTE_CMD_PREFIXES,
    VOLUME_CMD_SUFFIXES
)

_LOGGER = logging.getLogger(__name__)

# Zone command prefixes (now only for set commands like power on/off)
ZONE_PREFIXES = {
    "main": "",
    "zone2": "A",
    "zone3": "B"
}

# Power query suffixes (no prefix needed)
POWER_QUERY_SUFFIXES = {
    "main": "?P",
    "zone2": "?AP",
    "zone3": "?BP"
}

# Volume query suffixes (no prefix needed)
VOLUME_QUERY_SUFFIXES = {
    "main": "?V",
    "zone2": "?ZV",
    "zone3": "?YV"
}

# Power response patterns
POWER_PATTERNS = {
    "main": "PWR",
    "zone2": "APR",
    "zone3": "BPR"
}

# Volume response patterns
VOLUME_PATTERNS = {
    "main": "VOL",
    "zone2": "ZV",
    "zone3": "YV"
}

# Combined feature flags
SUPPORT_FLAGS = (
    MediaPlayerEntityFeature.TURN_ON
    | MediaPlayerEntityFeature.TURN_OFF
    | MediaPlayerEntityFeature.VOLUME_SET
    | MediaPlayerEntityFeature.VOLUME_MUTE
    | MediaPlayerEntityFeature.SELECT_SOURCE
)


async def async_setup_entry(hass, entry, async_add_entities):
    telnet = hass.data["pioneer_sc85"][entry.entry_id]
    entities = [
        PioneerZone(
            telnet=telnet,
            zone=name,
            prefix=ZONE_PREFIXES[name],
            power_query_suffix=POWER_QUERY_SUFFIXES[name],
            power_pattern=POWER_PATTERNS[name],
            volume_query_suffix=VOLUME_QUERY_SUFFIXES[name],
            volume_pattern=VOLUME_PATTERNS[name],
            volume_cmd_suffix=VOLUME_CMD_SUFFIXES[name],
            mute_query_suffix=MUTE_QUERY_SUFFIXES[name],
            mute_pattern=MUTE_PATTERNS[name],
            mute_cmd_prefix=MUTE_CMD_PREFIXES[name],
            input_query_suffix=INPUT_QUERY_SUFFIXES[name],
            input_cmd_suffix=INPUT_CMD_SUFFIXES[name],
            input_pattern=INPUT_PATTERNS[name],
            entry=entry,
        )
        for name in ZONE_PREFIXES
    ]
    async_add_entities(entities)


class PioneerZone(MediaPlayerEntity):
    _attr_has_entity_name = True

    def __init__(
        self,
        telnet,
        zone: str,
        prefix: str,
        power_query_suffix: str,
        power_pattern: str,
        volume_query_suffix: str,
        volume_pattern: str,
        volume_cmd_suffix: str,
        mute_query_suffix: str,
        mute_pattern: str,
        mute_cmd_prefix: str,
        input_query_suffix: str,
        input_cmd_suffix: str,
        input_pattern: str,
        entry,
    ):
        self.telnet = telnet
        self.zone = zone
        self.prefix = prefix  # Used only for set commands like power on/off
        self.power_query_suffix = power_query_suffix
        self.power_pattern = power_pattern
        self.volume_query_suffix = volume_query_suffix
        self.volume_pattern = volume_pattern
        self.volume_cmd_suffix = volume_cmd_suffix
        self.mute_query_suffix = mute_query_suffix
        self.mute_pattern = mute_pattern
        self.mute_cmd_prefix = mute_cmd_prefix
        self.input_query_suffix = input_query_suffix
        self.input_cmd_suffix = input_cmd_suffix
        self.input_pattern = input_pattern
        self.entry = entry

        # State
        self._state = MediaPlayerState.OFF
        self._volume_internal = 0
        self._muted = False
        self._source = None

        telnet.register(self._parse)

        # Query initial states
        asyncio.create_task(self._query_initial_state())

    async def _query_with_retry(self, query: str, max_attempts: int = 3, delay: float = 1.5):
        """Send a query with retries."""
        for attempt in range(1, max_attempts + 1):
            _LOGGER.debug("Sending query '%s' (attempt %d/%d) for %s", query, attempt, max_attempts, self.zone)
            await self.telnet.send(query + "\r")
            await asyncio.sleep(delay)
        _LOGGER.warning("No response to '%s' after %d attempts for %s", query, max_attempts, self.zone)

    async def _query_initial_state(self):
        await asyncio.sleep(10)  # Allow telnet to stabilize

        # Power (no prefix)
        power_query = self.power_query_suffix
        await self._query_with_retry(power_query)

        # Volume (no prefix)
        volume_query = self.volume_query_suffix
        await self._query_with_retry(volume_query)

        # Mute (no prefix)
        mute_query = self.mute_query_suffix
        await self._query_with_retry(mute_query)

        # Source (no prefix)
        source_query = self.input_query_suffix
        await self._query_with_retry(source_query)

    @property
    def unique_id(self) -> str:
        return f"{self.entry.entry_id}_{self.zone}"

    @property
    def device_info(self) -> DeviceInfo:
        return get_device_info(self.entry)

    @property
    def name(self):
        return self.zone.capitalize()

    @property
    def supported_features(self):
        return SUPPORT_FLAGS

    @property
    def state(self):
        return self._state

    @property
    def volume_level(self) -> float | None:
        if self.zone == "main":
            return (self._volume_internal - 1) / 179.0
        else:
            return (self._volume_internal - 1) / 80.0

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
        cmd = f"{self.prefix}PO"  # Prefix needed for set
        _LOGGER.debug("ON %s: %s", self.zone, cmd)
        await self.telnet.send(cmd + "\r")

    async def async_turn_off(self):
        cmd = f"{self.prefix}PF"  # Prefix needed for set
        _LOGGER.debug("OFF %s: %s", self.zone, cmd)
        await self.telnet.send(cmd + "\r")

    async def async_set_volume_level(self, volume: float):
        """Set volume level (0.0–1.0)."""
        _LOGGER.info("=== Volume set requested for %s ===", self.zone)
        _LOGGER.info("HA volume value: %.2f", volume)

        if self.zone == "main":
            level = int(volume * 179) + 1
            cmd = f"{level:03d}{self.volume_cmd_suffix}"
        else:
            level = int(volume * 80) + 1
            cmd = f"{level:02d}{self.volume_cmd_suffix}"

        _LOGGER.info("Calculated internal level: %d", level)
        _LOGGER.info("Command to send: '%s'", cmd)
        _LOGGER.info("Full sent string: '%s'", cmd + "\r")

        await self.telnet.send(cmd + "\r")

    async def async_mute_volume(self, mute: bool):
        suffix = "MO" if mute else "MF"
        cmd = f"{self.mute_cmd_prefix}{suffix}"
        _LOGGER.debug("Set mute %s: %s", self.zone, cmd)
        await self.telnet.send(cmd + "\r")

    async def async_select_source(self, source: str):
        """Select input source by friendly name."""
        input_key = next(
            (key for key, name in INPUTS.items() if name == source),
            None
        )
        if input_key is None:
            _LOGGER.warning("Unknown source '%s' for %s", source, self.zone)
            return

        input_code = input_key[:-2]
        cmd = f"{input_code}{self.input_cmd_suffix}"
        _LOGGER.debug("Setting source %s: %s (code: %s)", self.zone, cmd, input_code)
        await self.telnet.send(cmd + "\r")

    def _parse(self, msg: str):
        msg = msg.strip()
        if not msg:
            return
        _LOGGER.debug("Received for %s: %s", self.zone, msg)

        # Power
        if msg.startswith(self.power_pattern):
            if msg.endswith("0"):
                self._state = MediaPlayerState.ON
                _LOGGER.debug("%s power ON (0)", self.zone)
            elif msg.endswith("1"):
                self._state = MediaPlayerState.OFF
                _LOGGER.debug("%s power OFF (1)", self.zone)

        # Volume
        elif msg.startswith(self.volume_pattern):
            try:
                vol_str = msg[len(self.volume_pattern):]
                self._volume_internal = int(vol_str)
                _LOGGER.debug("%s volume parsed: %d", self.zone, self._volume_internal)
            except ValueError:
                _LOGGER.debug("Volume parse failed for %s: %s", self.zone, msg)

        # Mute
        elif msg.startswith(self.mute_pattern):
            if msg.endswith("0"):
                self._muted = True
                _LOGGER.debug("%s muted (0)", self.zone)
            elif msg.endswith("1"):
                self._muted = False
                _LOGGER.debug("%s unmuted (1)", self.zone)

        # Source
        elif msg.startswith(self.input_pattern):
            try:
                input_code = msg[len(self.input_pattern):]
                key = input_code + "FN"
                self._source = INPUTS.get(key)
                if self._source:
                    _LOGGER.debug("%s source parsed: %s (%s)", self.zone, self._source, input_code)
                else:
                    _LOGGER.warning("%s unknown source code: %s", self.zone, input_code)
            except Exception as e:
                _LOGGER.error("%s source parse error: %s", self.zone, e)

        self.schedule_update_ha_state()