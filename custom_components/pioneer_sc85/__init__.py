import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.const import Platform

from .const import DOMAIN

PLATFORMS = [Platform.MEDIA_PLAYER, Platform.SELECT, Platform.SENSOR, Platform.SWITCH]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Pioneer SC-85 from a config entry."""
    # Store the telnet connection (assuming it's created elsewhere, e.g., in a hub)
    # hass.data.setdefault(DOMAIN, {})[entry.entry_id] = api

    # Create the device
    device_registry = dr.async_get(hass)
    device_registry.async_get_or_create(
        config_entry_id=entry.entry_id,
        identifiers={(DOMAIN, entry.entry_id)},
        name="Pioneer SC-85 Receiver",
        manufacturer="Pioneer",
        model="SC-85",
        configuration_url=f"http://{entry.data['host']}",
    )

    # Forward to platforms
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Optional: Add cleanup
    entry.async_on_unload(entry.add_update_listener(async_update_listener))

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    return True

async def async_update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update."""
    await hass.config_entries.async_reload(entry.entry_id)