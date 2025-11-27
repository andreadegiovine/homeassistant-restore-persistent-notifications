# HomeAssistant - Restore Persistent Notification
- [Features](#features)
- [Installation](#installation)

This integration use the **HomeAssistant core** to store [**persistent notifications**](https://www.home-assistant.io/integrations/persistent_notification/) in a sensor entity, when the system is rebooted the persistent notifications are restored.

## Features
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
<details><summary><b>Using HACS</b></summary>

1. Go to [HACS](https://hacs.xyz/) section;
2. Search and install **Restore Persistent Notification** from the HACS integration list;
3. Add this integration from the **Home Assistant** integrations.

</details>
<details><summary><b>Manually</b></summary>

1. Download this repository;
2. Copy the directory **custom_components/restore_persistent_notifications** on your Home Assistant **config/custom_components/restore_persistent_notifications**;
3. Restart HomeAssistant;
4. Add this integration from the **Home Assistant** integrations.

</details>

## Support the project
**The latest heroes who believe in this project** 👇

**🏆 5 beers**  
Someone  
exi  
Philipp B. / tamcore  
<sub>*and other heroes*</sub>

**🥈 3 beers**  
John Woertman  
Pekka  
Gerhard  
<sub>*and other heroes*</sub>

**🥉 2 beers**  
Grosi001  
ryhaberecht  
Tizian  

**⭐ 1 beers**  
teknohead  
@bgoncal2  
Max  
<sub>*and other heroes*</sub>

### Want to join the Club?
[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/andreatito)  
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/W7W11C9QJ7)
