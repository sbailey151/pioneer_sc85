"""Constants for Pioneer SC-85 integration."""

DOMAIN = "pioneer_sc85"
DEFAULT_PORT = 23
DEFAULT_HOST = "192.168.128.183"

from homeassistant.helpers.device_registry import DeviceInfo


def get_device_info(entry) -> DeviceInfo:
    """Return device information to be used in entity device_info."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Pioneer SC-85 Receiver",
        manufacturer="Pioneer",
        model="SC-85",
        configuration_url=f"http://{entry.data['host']}",
    )


ZONES = {
    "main": "MZ",
    "zone2": "Z2",
    "zone3": "Z3"
}

INPUTS = {
    "01FN": "CD",
    "02FN": "Tuner",
    "05FN": "TV",
    "04FN": "DVD",
    "25FN": "Blu-ray",
    "06FN": "TV/SAT",
    "17FN": "iPod/USB",
    "15FN": "DVR/BDR",
    "22FN": "HDMI 4",
    "23FN": "HDMI 5",
    "24FN": "HDMI 6",
    "34FN": "HDMI 7/MHL",
    "33FN": "Adapter Port",
    "38FN": "Internet Radio",
    "45FN": "Favorites",
    "41FN": "Pandora",
    "44FN": "Media Server"
}

DSP_MODES = {
    "0001SR": "Stereo",
    "0005SR": "Stereo (Rotating)",
    "0006SR": "Auto Surround",
    "0009SR": "Stereo 2",
    "0010SR": "Dolby Surround (Rotating)",
    "0038SR": "NEO:X Music",
    "0039SR": "NEO:X Game",
    "0050SR": "Dolby Surround",
    "0100SR": "Action (Rotating)",
    "0101SR": "Action",
    "0103SR": "Drama",
    "0107SR": "Classical",
    "0110SR": "Rock/Pop",
    "0112SR": "Ext. Stereo",
    "0117SR": "Sports",
    "0118SR": "Advanced Game",
    "0151SR": "ALC",
    "0152SR": "Optimum Surround",
    "0200SR": "Eco Mode (Rotating)",
    "0212SR": "Eco Mode 1",
    "0213SR": "Eco Mode 2",
    "0006SR": "Auto Surround",
    "0007SR": "Direct",
    "0008SR": "Pure Direct",
    "0037SR": "NEO:X Cinema",
    "0003SR": "F.S. Surround"
}

AUDIO_FORMATS = {
    "01": "PCM",
    "02": "Dolby Digital",
    "03": "DTS",
    "04": "Dolby TrueHD",
    "05": "DTS-HD MA",
    "06": "Atmos"
}

# --- Source handling constants ---
# Suffixes for setting source (code + suffix)
INPUT_CMD_SUFFIXES = {
    "main": "FN",
    "zone2": "ZS",
    "zone3": "ZT"
}

# Patterns for parsing source responses
INPUT_PATTERNS = {
    "main": "FN",
    "zone2": "ZS",
    "zone3": "ZT"
}

# Suffixes for querying source
INPUT_QUERY_SUFFIXES = {
    "main": "?F",
    "zone2": "?ZS",
    "zone3": "?ZT"
}

# Mute query suffixes and patterns
MUTE_QUERY_SUFFIXES = {
    "main": "?M",
    "zone2": "?Z2M",
    "zone3": "?Z3M"
}
"""Constants for Pioneer SC-85 integration."""

DOMAIN = "pioneer_sc85"
DEFAULT_PORT = 23
DEFAULT_HOST = "192.168.128.183"

from homeassistant.helpers.device_registry import DeviceInfo


def get_device_info(entry) -> DeviceInfo:
    """Return device information to be used in entity device_info."""
    return DeviceInfo(
        identifiers={(DOMAIN, entry.entry_id)},
        name="Pioneer SC-85 Receiver",
        manufacturer="Pioneer",
        model="SC-85",
        configuration_url=f"http://{entry.data['host']}",
    )


ZONES = {
    "main": "MZ",
    "zone2": "Z2",
    "zone3": "Z3"
}

INPUTS = {
    "01FN": "CD",
    "02FN": "Tuner",
    "05FN": "TV",
    "04FN": "DVD",
    "25FN": "Blu-ray",
    "06FN": "TV/SAT",
    "17FN": "iPod/USB",
    "15FN": "DVR/BDR",
    "22FN": "HDMI 4",
    "23FN": "HDMI 5",
    "24FN": "HDMI 6",
    "34FN": "HDMI 7/MHL",
    "33FN": "Adapter Port",
    "38FN": "Internet Radio",
    "45FN": "Favorites",
    "41FN": "Pandora",
    "44FN": "Media Server"
}

DSP_MODES = {
    "0001SR": "Stereo",
    "0005SR": "Stereo (Rotating)",
    "0006SR": "Auto Surround",
    "0009SR": "Stereo 2",
    "0010SR": "Dolby Surround (Rotating)",
    "0038SR": "NEO:X Music",
    "0039SR": "NEO:X Game",
    "0050SR": "Dolby Surround",
    "0100SR": "Action (Rotating)",
    "0101SR": "Action",
    "0103SR": "Drama",
    "0107SR": "Classical",
    "0110SR": "Rock/Pop",
    "0112SR": "Ext. Stereo",
    "0117SR": "Sports",
    "0118SR": "Advanced Game",
    "0151SR": "ALC",
    "0152SR": "Optimum Surround",
    "0200SR": "Eco Mode (Rotating)",
    "0212SR": "Eco Mode 1",
    "0213SR": "Eco Mode 2",
    "0006SR": "Auto Surround",
    "0007SR": "Direct",
    "0008SR": "Pure Direct",
    "0037SR": "NEO:X Cinema",
    "0003SR": "F.S. Surround"
}

AUDIO_FORMATS = {
    "01": "PCM",
    "02": "Dolby Digital",
    "03": "DTS",
    "04": "Dolby TrueHD",
    "05": "DTS-HD MA",
    "06": "Atmos"
}

# --- Source handling constants ---
# Suffixes for setting source (code + suffix)
INPUT_CMD_SUFFIXES = {
    "main": "FN",
    "zone2": "ZS",
    "zone3": "ZT"
}

# Patterns for parsing source responses
INPUT_PATTERNS = {
    "main": "FN",
    "zone2": "ZS",
    "zone3": "ZT"
}

# Suffixes for querying source
INPUT_QUERY_SUFFIXES = {
    "main": "?F",
    "zone2": "?ZS",
    "zone3": "?ZT"
}

# Mute query suffixes and patterns
MUTE_QUERY_SUFFIXES = {
    "main": "?M",
    "zone2": "?Z2M",
    "zone3": "?Z3M"
}

MUTE_PATTERNS = {
    "main": "MUT",
    "zone2": "Z2MUT",
    "zone3": "Z3MUT"
}

# Mute command prefixes
MUTE_CMD_PREFIXES = {
    "main": "",
    "zone2": "Z2",
    "zone3": "Z3"
}

# Volume command suffixes (level + suffix)
VOLUME_CMD_SUFFIXES = {
    "main": "VL",
    "zone2": "ZV",
    "zone3": "YV"
}