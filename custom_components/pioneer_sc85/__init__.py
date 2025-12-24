"""Pioneer SC-85 integration entry point."""
from .const import DOMAIN
from .telnet import PioneerTelnet

PLATFORMS = ["media_player", "select", "switch", "sensor"]

async def async_setup(hass, config):
    """Default setup for HA; needed to avoid setup errors."""
    return True

async def async_setup_entry(hass, entry):
    """Set up Pioneer SC-85 from a config entry."""
    telnet = PioneerTelnet(entry.data["host"], entry.data["port"])
    await telnet.connect()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = telnet

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
