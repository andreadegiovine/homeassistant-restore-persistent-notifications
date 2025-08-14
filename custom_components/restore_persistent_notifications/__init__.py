"""Component to integrate with persist_persistent_notifications."""

import logging
import asyncio
from .const import (
        DOMAIN,
        SENSOR_PLATFORM,
        SENSOR
)
from homeassistant.components.persistent_notification import _async_get_or_create_notifications
_LOGGER = logging.getLogger(__name__)

def setup(hass, config):
    """Set up this component using YAML."""
    if config.get(DOMAIN) is None:
        # We get here if the integration is set up using config flow
        return True

async def async_setup_entry(hass, entry):
    """Set up this component using YAML."""
    #init the sensor entity
    _LOGGER.debug("in __init__ : async_setup_entry")
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, SENSOR_PLATFORM))

    async def erase_and_save_notifications(event):
        try:
          hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR].reset_persistent_notifications()
          await save_notifications(event)
        except Exception as err:
          _LOGGER.error("Error is" + str(err))
          raise
        except:
          _LOGGER.error("Oups")
          raise

    async def save_notifications(event):
        """ retrieve the persistent notification and store them in the sensor """
        _LOGGER.debug("saving persistent notification")
        sensor = hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR]
        try:
            notifications = _async_get_or_create_notifications(hass)
            for notif in notifications:
            #for pn_id in hass.states.async_entity_ids("persistent_notification"):
                pn = notifications[notif]
                _LOGGER.debug("Getting persistent notification "+pn["notification_id"])
                _LOGGER.debug("Message is "+pn["message"])
                await sensor.async_add_persistent_notification(pn["notification_id"], pn["title"], pn["message"])
        except Exception as err:
          _LOGGER.error("Error is" + str(err))
          raise
        except:
          _LOGGER.error("Oups")
          raise
        _LOGGER.debug("persistent notification saved")

    async def restore_notifications(event):
        """ recreate the persistent notification based on the sensor attributes """
        return
        _LOGGER.debug("restoring persistent notification")
        sensor = hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR]
        for pn in sensor.persistent_notifications:
            service_data = {}
            service_data["message"] = pn["message"]
            if "title" in pn:
                service_data["title"] = pn["title"]
            #do not generate an id
            await hass.services.async_call("persistent_notification", "create", service_data, blocking=False)


    hass.bus.async_listen("homeassistant_stop", erase_and_save_notifications)
    #hass.bus.listen_once("homeassistant_stop", erase_and_save_notifications)
    #also on the persistent_notification in case HA is not shut own gently
    #call erase_and_save and not just save to deal with dismiss & dismiss all
    hass.bus.async_listen("persistent_notifications_updated", erase_and_save_notifications)
    hass.bus.async_listen("homeassistant_start", restore_notifications)
    #restore_notifications(None)

    return True
