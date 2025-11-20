import logging

from homeassistant import config_entries

from .const import ( DOMAIN, NAME )

_LOGGER = logging.getLogger(__name__)

class RestorePersistentNotificationsConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_create_flow(handler, context, data):
        """Create flow."""
        pass

    async def async_finish_flow(flow, result):
        """Finish flow."""
        pass

    async def async_step_user(self, info=None):
        await self.async_set_unique_id(DOMAIN)
        self._abort_if_unique_id_configured()
        return self.async_create_entry(title=NAME, data={})

