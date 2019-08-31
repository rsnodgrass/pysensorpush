"""Constants used by PySensorPush"""

API_URL = 'https://api.sensorpush.com/api/v1'

OAUTH_AUTHORIZE_ENDPOINT = API_URL + '/oauth/authorize'
OAUTH_TOKEN_ENDPOINT     = API_URL + '/oauth/accesstoken'
LIST_GATEWAYS_ENDPOINT   = API_URL + '/devices/gateways'
LIST_SENSORS_ENDPOINT    = API_URL + '/devices/sensors'
QUERY_SAMPLES_ENDPOINT   = API_URL + '/samples'
