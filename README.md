# pysensorpush - Python interface for the SensorPush API

Python implementation of the [SensorPush temperature and humidity/hygrometer sensors](https://www.amazon.com/SensorPush-Wireless-Thermometer-Hygrometer-Android/dp/B01AEQ9X9I?tag=rynoshark-20) cloud API which
supports both temperature (&deg;F) and humidity (Rh) sensors. 

[![PyPi](https://img.shields.io/pypi/v/pysensorpush.svg)](https://pypi.python.org/pypi/pysensorpush)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=WREP29UDAMB6G)

NOTE: Ideally SensorPush sensors would be located within range of a [SensorPush G1 WiFi Gateway](https://www.amazon.com/SensorPush-G1-WiFi-Gateway-Anywhere/dp/B01N17RWWV?tag=rynoshark-20) for continously collecting and publishing data from the sensors to the SensorPush cloud. However, SensorPush sensors can also synchronize historical data over Bluetooth when nearby to an iOS or Android device with the SensorPush app.

## Installation

```
pip3 install pysensorpush
```

## Enable the SensorPush API

While the SensorPush API is in beta, you may need to contact [support@sensorpush.com](mailto:support@sensorpush.com?subject=[api]) to get access to the API for your account. Here are details direct from SensorPush:

> If you're ready to use the beta of the SensorPush API, please review the updated Terms of Service at this link on our website (http://www.sensorpush.com/legal/info). 
>
> These Terms are based largely on the Terms of Service already in place. The primary difference is that we added language to cover the API, so if you accept these terms, please respond to support@sensorpush.com with the following:
>
> 1.) Confirmation:  "Yes, I accept these Terms of Service"
> 2.) Your Gateway email address
>
> We need these two things so we can grant you access to the API.
>
> If you have any questions. Please just send them to support@sensorpush.com and include "[api]" in the subject

## Examples

```python
sensorpush = PySensorPush(username, password)

sensorpush.gateways

sensorpush.sensors

sensorpush.samples(10)
```

See also [example-client.py](example-client.py) for a working example.

## See Also

* [SensorPush API Docs](http://www.sensorpush.com/api/docs)
* [SensorPush for Home Assistant](https://github.com/rsnodgrass/hass-sensorpush)

#### Hardware

* [SensorPush Wireless Thermometer/Hygrometer - Humidity & Temperature Smart Sensor](https://www.amazon.com/SensorPush-Wireless-Thermometer-Hygrometer-Android/dp/B01AEQ9X9I?tag=rynoshark-20)
* [SensorPush G1 WiFi Gateway](https://www.amazon.com/SensorPush-G1-WiFi-Gateway-Anywhere/dp/B01N17RWWV?tag=rynoshark-20)
* [SensorPush](https://sensorpush.com) (official product page)

## Future Enhancements

* improve error handling/edge conditions

* allow fetching data directly from the sensor via Bluetooth (no cloud dependency required)
