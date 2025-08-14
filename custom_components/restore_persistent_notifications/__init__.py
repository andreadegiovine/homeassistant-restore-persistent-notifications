"""Component to integrate with persist_persistent_notifications."""

import logging
import asyncio
from .const import (
        DOMAIN,
        SENSOR_PLATFORM,
        SENSOR
)
from homeassistant.components.persistent_notification import _async_get_or_create_notifications
from homeassistant.components.persistent_notification import ( ATTR_CREATED_AT, ATTR_MESSAGE, ATTR_NOTIFICATION_ID, ATTR_TITLE )
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
    hass.async_create_task(hass.config_entries.async_forward_entry_setups(entry, [SENSOR_PLATFORM]))

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
                _LOGGER.debug("Getting persistent notification "+pn[ATTR_NOTIFICATION_ID])
                _LOGGER.debug("Message is "+pn[ATTR_MESSAGE])
                await sensor.async_add_persistent_notification(pn[ATTR_NOTIFICATION_ID], pn[ATTR_TITLE], pn[ATTR_MESSAGE], pn[ATTR_CREATED_AT])
        except Exception as err:
          _LOGGER.error("Error is" + str(err))
          raise
        except:
          _LOGGER.error("Oups")
          raise
        _LOGGER.debug("persistent notification saved")

    # async def restore_notifications(event):
    #     """ recreate the persistent notification based on the sensor attributes """
    #     _LOGGER.debug("restoring persistent notification")
    #     sensor = hass.data[DOMAIN][SENSOR_PLATFORM][SENSOR]
    #     for pn in sensor.persistent_notifications:
    #         service_data = {}
    #         service_data[ATTR_MESSAGE] = pn[ATTR_MESSAGE]
    #         if ATTR_TITLE in pn:
    #             service_data[ATTR_TITLE] = pn[ATTR_TITLE]
    #         if ATTR_CREATED_AT in pn:
    #             service_data[ATTR_CREATED_AT] = pn[ATTR_CREATED_AT]
    #         if ATTR_NOTIFICATION_ID in pn:
    #             service_data[ATTR_NOTIFICATION_ID] = pn[ATTR_NOTIFICATION_ID]
    #         _LOGGER.debug("calling persistent notif create")
    #         await hass.services.async_call("persistent_notification", "create", service_data, blocking=False)


    hass.bus.async_listen("homeassistant_stop", erase_and_save_notifications)
    #hass.bus.listen_once("homeassistant_stop", erase_and_save_notifications)
    #also on the persistent_notification in case HA is not shut own gently
    #call erase_and_save and not just save to deal with dismiss & dismiss all
    hass.bus.async_listen("persistent_notifications_updated", erase_and_save_notifications)
    # hass.bus.async_listen("homeassistant_start", restore_notifications)
    #restore_notifications(None)

    return True
