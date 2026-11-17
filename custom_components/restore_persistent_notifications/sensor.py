import logging
from datetime import datetime

from homeassistant.core import HomeAssistant, callback
from homeassistant.config_entries import ConfigEntry
from homeassistant.components.sensor import RestoreSensor, SensorEntityDescription
from homeassistant.components.persistent_notification import (
    ATTR_CREATED_AT,
    ATTR_MESSAGE,
    ATTR_NOTIFICATION_ID,
    ATTR_TITLE,
    UpdateType,
    _async_get_or_create_notifications,
    async_create,
    async_register_callback,
)
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.util import dt as dt_util

from .const import DOMAIN, NAME, SENSOR_KEY, SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY, RESTORED_MESSAGE_SUFFIX

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    description = SensorEntityDescription(
        key=SENSOR_KEY,
        name=SENSOR_KEY,
        translation_key=SENSOR_KEY,
    )
    async_add_entities([RestorePersistentNotifications(description)])


class RestorePersistentNotifications(RestoreSensor):
    _attr_should_poll = False
    _attr_has_entity_name = False
    # Notifications are persisted by the restore state storage, keep them out of the recorder database
    _unrecorded_attributes = frozenset({SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY})

    def __init__(self, description: SensorEntityDescription):
        self.entity_description = description
        self._attr_unique_id = description.key
        self._attr_translation_key = description.translation_key
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY: []}
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, NAME)},
            name=NAME,
            entry_type=DeviceEntryType.SERVICE,
        )

    async def async_added_to_hass(self):
        _LOGGER.debug("async_added_to_hass")
        await super().async_added_to_hass()

        notifications = []
        if (restored_data := await self.async_get_last_state()) is not None:
            notifications = restored_data.attributes.get(SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY) or []

        self._restore_notifications(notifications)

        # Listen to every notification change (services, integrations, frontend dismiss, ...)
        self.async_on_remove(async_register_callback(self.hass, self._async_notifications_updated))

        self._save_notifications()

    @callback
    def _async_notifications_updated(self, update_type: UpdateType, notifications: dict) -> None:
        _LOGGER.debug(f"Notifications updated: {update_type}")
        self._save_notifications()

    @callback
    def _save_notifications(self) -> None:
        notifications = []
        for notify in _async_get_or_create_notifications(self.hass).values():
            notify_data = dict(notify)
            created_at = notify_data.get(ATTR_CREATED_AT)
            if isinstance(created_at, datetime):
                notify_data[ATTR_CREATED_AT] = created_at.isoformat()
            notifications.append(notify_data)

        _LOGGER.debug(f"Save notifications: {len(notifications)}")

        self._attr_native_value = len(notifications)
        self._attr_extra_state_attributes = {SENSOR_NOTIFICATIONS_ATTRIBUTE_KEY: notifications}
        self.async_write_ha_state()

    @callback
    def _restore_notifications(self, notifications: list) -> None:
        _LOGGER.debug(f"Restore notifications: {len(notifications)}")

        core_notifications = _async_get_or_create_notifications(self.hass)

        for notify in notifications:
            try:
                notification_id = notify[ATTR_NOTIFICATION_ID]
                if notification_id in core_notifications:
                    # Already recreated by someone else during startup, keep the newest one
                    continue

                message = notify[ATTR_MESSAGE] or ""
                if RESTORED_MESSAGE_SUFFIX not in message:
                    message = message + RESTORED_MESSAGE_SUFFIX

                async_create(self.hass, message, notify.get(ATTR_TITLE), notification_id)

                created_at = notify.get(ATTR_CREATED_AT)
                if isinstance(created_at, str):
                    created_at = dt_util.parse_datetime(created_at)
                if isinstance(created_at, datetime):
                    core_notifications[notification_id][ATTR_CREATED_AT] = created_at
            except Exception as e:
                _LOGGER.error(f"Restore notification error ({notify}): {e}")
