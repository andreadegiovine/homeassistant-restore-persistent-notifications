import logging
from datetime import timedelta

from homeassistant.core import ( HomeAssistant, Event )
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EVENT_CALL_SERVICE
from homeassistant.components.persistent_notification import DOMAIN as PERSISTENT_NOTIFICATION_DOMAIN
from homeassistant.components.notify.const import SERVICE_NOTIFY as NOTIFY_DOMAIN
from homeassistant.components.notify.const import SERVICE_PERSISTENT_NOTIFICATION as NOTIFY_PERSISTENT_NOTIFICATION
from homeassistant.helpers.event import async_track_point_in_time
from homeassistant.util import dt as dt_util

from .const import ( DOMAIN, SENSOR_PLATFORM, SENSOR_KEY )

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, config: ConfigEntry):
    _LOGGER.debug("async_setup_entry")

    await hass.config_entries.async_forward_entry_setups(config, [SENSOR_PLATFORM])


    async def save_notifications(event: Event):
        _LOGGER.debug("listen_events")

        domain = event.data["domain"]
        service = event.data["service"]

        _LOGGER.debug(f"Domain: {domain}")
        _LOGGER.debug(f"Service: {service}")

        if domain == PERSISTENT_NOTIFICATION_DOMAIN or (domain == NOTIFY_DOMAIN and service == NOTIFY_PERSISTENT_NOTIFICATION):

            point_in_time = dt_util.utcnow() + timedelta(seconds=1)

            async def save_notifications(now):
                try:
                    sensor = hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR_KEY]
                    await sensor.save_notifications()
                except Exception as e:
                    _LOGGER.error(f"Save notifications error: {e}")

            async_track_point_in_time(hass, save_notifications, point_in_time)

        return True

    hass.bus.async_listen(EVENT_CALL_SERVICE, save_notifications)

    return True
