from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, DEFAULT_PORT, DEFAULT_HOST

class PioneerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input:
            return self.async_create_entry(
                title="Pioneer SC-85",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host", default=DEFAULT_HOST): str,
                vol.Optional("port", default=DEFAULT_PORT): int
            })
        )
