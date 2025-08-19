import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import ( RestoreSensor, SensorEntityDescription )
from homeassistant.components.persistent_notification import _async_get_or_create_notifications
from homeassistant.components.persistent_notification import ( ATTR_CREATED_AT, ATTR_NOTIFICATION_ID )

from .const import ( DOMAIN, NAME, SENSOR_PLATFORM, SENSOR_KEY, SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY )

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry, async_add_entities):
    sensors = []

    description = SensorEntityDescription(
        key=SENSOR_KEY,
        name=SENSOR_KEY,
        translation_key = SENSOR_KEY
    )
    sensors.extend([RestorePersistentNotifications(hass, description)])

    async_add_entities(sensors)


class RestorePersistentNotifications(RestoreSensor):
    def __init__(self, hass, description):
        self._hass = hass

        self.entity_description = description
        self._attr_unique_id = description.key
        self._attr_native_value = 0
        self._available = True
        self._attr_extra_state_attributes = {}
        self._attr_translation_key = description.translation_key
        self._attr_has_entity_name = False


    @property
    def device_info(self):
        return {
            "identifiers": {
                (DOMAIN, NAME)
            },
            "name": NAME
        }


    async def async_added_to_hass(self):
        _LOGGER.debug("async_added_to_hass")

        restored_data = await self.async_get_last_state()
        notifications = []

        if restored_data:
            self._attr_native_value = restored_data.state
            if SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY in restored_data.attributes:
                notifications = restored_data.attributes[SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY]

        self._attr_extra_state_attributes[SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY] = notifications

        if DOMAIN not in self._hass.data:
            self._hass.data[DOMAIN] = {}
        if SENSOR_PLATFORM not in self._hass.data[DOMAIN]:
            self._hass.data[DOMAIN][SENSOR_PLATFORM] = {}
        self._hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR_KEY] = self

        await self.restore_notifications()


    async def save_notifications(self):
        _LOGGER.debug("save_notifications")

        self._attr_extra_state_attributes[SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY] = []
        self._attr_native_value = 0
        self.async_write_ha_state()

        notifications = _async_get_or_create_notifications(self._hass)
        notifications_count = int(len(notifications))

        _LOGGER.debug(f"Count: {notifications_count}")
        _LOGGER.debug(f"Notifications: {notifications}")

        if notifications_count > 0:
            self._attr_native_value = notifications_count

            for notify in notifications:
                _LOGGER.debug(f"Save notification: {notify}")
                self._attr_extra_state_attributes[SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY].append(notifications[notify])

            self.async_write_ha_state()


    async def restore_notifications(self):
        _LOGGER.debug("restore_notifications")

        core_notifications = _async_get_or_create_notifications(self._hass)

        notifications = self._attr_extra_state_attributes[SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY]
        notifications_count = int(len(notifications))

        _LOGGER.debug(f"Count: {notifications_count}")
        _LOGGER.debug(f"Notifications: {notifications}")

        if notifications_count > 0:
            try:
                for notify in notifications:
                    notify_data = notify.copy()
                    _LOGGER.debug(f"Restore notification: {notify_data[ATTR_NOTIFICATION_ID]}")
                    del notify_data[ATTR_CREATED_AT]
                    await self.hass.services.async_call("persistent_notification", "create", notify_data, blocking=False)
                    core_notifications[notify_data[ATTR_NOTIFICATION_ID]][ATTR_CREATED_AT] = notify[ATTR_CREATED_AT]

            except Exception as e:
                _LOGGER.error(f"Restore notifications error: {e}")
