from homeassistant import config_entries
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class PersistPersistentNotificationConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    async def async_create_flow(handler, context, data):
        """Create flow."""
        pass

    async def async_finish_flow(flow, result):
        """Finish flow."""
        pass

    async def async_step_user(self, info=None):
        return self.async_create_entry(title="Persist Persistent Notification", data={})

