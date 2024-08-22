
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import DOMAIN

@config_entries.HANDLERS.register(DOMAIN)
class SwissPostScrappingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Swiss Post Scrapping."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title="Swiss Post Scrapping", data=user_input)

        # Define the form schema with email and password
        data_schema = vol.Schema({
            vol.Required("email"): str,
            vol.Required("password"): str,
            vol.Required("interval", default=5): int,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return SwissPostScrappingOptionsFlow(config_entry)


class SwissPostScrappingOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Swiss Post Scrapping."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        
        # Retrieve the current options
        options = {
            vol.Required("email", default=self.config_entry.options.get("email", "")): str,
            vol.Required("password", default=self.config_entry.options.get("password", "")): str,
            vol.Required("interval", default=self.config_entry.options.get("interval", 5)): int,
        }

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(options)
        )