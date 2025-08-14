from homeassistant.helpers.restore_state import RestoreEntity
#from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.core import callback
from homeassistant.components.persistent_notification import ( ATTR_CREATED_AT, ATTR_MESSAGE, ATTR_NOTIFICATION_ID, ATTR_TITLE )
import asyncio
import logging
from .const import (
        DOMAIN,
        SENSOR_PLATFORM,
        SENSOR
)
_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, _, async_add_entities, discovery_info=None):
    """Create presence simulation entity defined in YAML and add them to HA."""
    _LOGGER.debug("async_setup_platform")
    if PersistPersistentNotifications.instances == 0:
        async_add_entities([PersistPersistentNotifications(hass)], True)


async def async_setup_entry(hass, config_entry, async_add_devices):
    _LOGGER.debug("async_setup_entry")
    """Create presence simulation entities defined in config_flow and add them to HA."""
    if PersistPersistentNotifications.instances == 0:
        async_add_devices([PersistPersistentNotifications(hass)], True)

class PersistPersistentNotifications(RestoreEntity):
    instances = 0

    def __init__(self, hass):
        self.hass = hass
        self.attr={}
        self._state = "0"
        PersistPersistentNotifications.instances += 1
        self.attr["persistent_messages"] = []

    @property
    def name(self):
        return "Persist Persistent Notifications"

    @property
    def state(self):
        """Return the state of the switch"""
        return self._state

    @property
    def extra_state_attributes(self):
        """Returns the attributes list"""
        return self.attr

    async def async_update(self):
        pass

    def update(self):
        pass

    @property
    def device_state_attributes(self):
        """Returns the attributes list"""
        return self.attr

    async def async_added_to_hass(self):
        """When sensor is added to hassio."""
        await super().async_added_to_hass()
        prev_state = await self.async_get_last_state()
        if prev_state is not None:
            self._state = prev_state.state
            if "persistent_messages" in prev_state.attributes:
                self.attr = prev_state.as_dict()["attributes"]

        _LOGGER.debug("restore state: %s", prev_state)
        if DOMAIN not in self.hass.data:
            self.hass.data[DOMAIN] = {}
        if SENSOR_PLATFORM not in self.hass.data[DOMAIN]:
            self.hass.data[DOMAIN][SENSOR_PLATFORM] = {}
        self.hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR] = self

        #the creation of the notif is done in __init__ restore_notifications
        for pn in self.persistent_notifications:
            service_data = {}
            service_data[ATTR_MESSAGE] = pn[ATTR_MESSAGE]
            if ATTR_TITLE in pn:
                service_data[ATTR_TITLE] = pn[ATTR_TITLE]
            if ATTR_CREATED_AT in pn:
                service_data[ATTR_CREATED_AT] = pn[ATTR_CREATED_AT]
            if ATTR_NOTIFICATION_ID in pn:
                service_data[ATTR_NOTIFICATION_ID] = pn[ATTR_NOTIFICATION_ID]
            _LOGGER.debug("calling persistent notif create")
            await self.hass.services.async_call("persistent_notification", "create", service_data, blocking=False)

    @callback
    def _schedule_immediate_update(self):
        self.async_schedule_update_ha_state(True)

    async def async_add_persistent_notification(self, notification_id, title, message, created_at):
        self._state += 1
        try:
            _LOGGER.debug("Adding persistent notification: " + message)
            self.attr["persistent_messages"].append({ATTR_MESSAGE: message, ATTR_NOTIFICATION_ID: notification_id, ATTR_TITLE: title, ATTR_CREATED_AT: created_at})
        except Exception as err:
            _LOGGER.error("Oups, error is" + str(err))


    @property
    def persistent_notifications(self):
        return self.attr["persistent_messages"]

    def reset_persistent_notifications(self):
        self.attr["persistent_messages"].clear()
        self._state = 0

    #unused
    async def is_new(self, notification):
        if ATTR_NOTIFICATION_ID in notification is not None:
            for notif in self.attr["persistent_messages"]:
                #await asyncio.sleep(0)
                if notif[ATTR_NOTIFICATION_ID] == notification[ATTR_NOTIFICATION_ID]:
                    return False
            return True
        for notif in self.attr["persistent_messages"]:
            #asyncio asyncio.sleep(0)
            if notif[ATTR_MESSAGE] == notification[ATTR_MESSAGE]:
                return False
        return True
