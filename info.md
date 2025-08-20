# HomeAssistant - Restore Persistent Notification
This integration use the **HomeAssistant core** to store [**persistent notifications**](https://www.home-assistant.io/integrations/persistent_notification/) in a sensor entity, when the system is rebooted the persistent notifications are restored.

Persistent notifications are saved when the following actions are triggered:
- persistent_notification.create
- persistent_notification.dismiss
- persistent_notification.dismiss_all
- notify.persistent_notification

When a persistent notification is retrieved, the following suffix is added after the **message** body:
```yaml
<!--- restored -->
```
The added suffix will not be shown in the HomeAssistant persistent notifications panel, but it is useful for automations or other operations such as:
```yaml
...
  - condition: template
    value_template: |-
      {{ not (notify_message is search('<!--- restored -->')) }}
...
```

## Installation
### Using [HACS](https://hacs.xyz/) 
1. Go to HACS section;
2. From the 3 dots menu (top right) click on **Add custom repository**;
3. Add as **Integration** this url https://github.com/andreadegiovine/homeassistant-restore-persistent-notifications;
4. Search and install **Restore Persistent Notification** from the HACS integration list;
5. Add this integration from the **Home Assistant** integrations.

### Manually
1. Download this repository;
2. Copy the directory **custom_components/restore_persistent_notifications** on your Home Assistant **config/custom_components/restore_persistent_notifications**;
3. Restart HomeAssistant;
4. Add this integration from the **Home Assistant** integrations.

## Support the project
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/andreatito)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W11C9QJ7)