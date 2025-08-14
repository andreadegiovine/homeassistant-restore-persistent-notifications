# Persist the persistent notification after Home Assistant shutdown
In HA behavior, the "persistent notifications" are cleared after a reboot. This custom component aim to save the notifications and restore them after a reboot.

The persistent notification will be saved in a new sensor `sensor.persist_persistent_notifications` when shutting down, and restored from this sensor after HA has restarted.

# Installation
- In your Home Assistant configuration directory (~/.homeassistant), create a directory custom_components if not already existing and navigate in it.
- `git clone https://github.com/slashback100/persist_persistent_notifications.git`
- Restart Home Assistant

# Configuration
- In the UI, go in Configuration > Integration
- Click on the '+' button
- Search for "Persist Persistent Notifications"
- Confirm
