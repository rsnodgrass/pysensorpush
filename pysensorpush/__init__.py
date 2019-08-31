"""Base Python Class file for SensorPush."""

import logging
import requests

from pysensorpush.sensor import SPSensor
from pysensorpush.const import ( OAUTH_AUTHORIZE_ENDPOINT, LIST_SENSORS_ENDPOINT )

LOG = logging.getLogger(__name__)

class PySensorPush(object):
    """Base object for SensorPush."""

    def __init__(self, username=None, password=None):
        """Create a PySensorPush object.
        :param username: SensorPush user email
        :param password: SensorPush user password
        :returns PySensorPush base object
        """
        self.authenticated = None
        self.date_created = None
        self.userid = None
        self.__token = None
        self.__headers = None
        self.__params = None

        self._all_gateways = {}
        self._all_sensors = {}

        # set username and password
        self.__password = password
        self.__username = username
        self.session = requests.Session()

        # login user
        self.login()

    def __repr__(self):
        """Object representation."""
        return "<{0}: {1}>".format(self.__class__.__name__, self.userid)

    def login(self):
        """Login to the SensorPush account."""
        LOG.debug("Creating SensorPush session")
        self._authenticate()

    def _authenticate(self):
        """Authenticate user and generate token."""
        self.reset_headers()
        data = self.query(
            OAUTH_AUTHORIZE_ENDPOINT,
            method='POST',
            extra_params={
                'email':    self.__username,
                'password': self.__password
            })

        if isinstance(data, dict) and data.get('success'):
            data = data.get('data')
            self.authenticated = data.get('authenticated')
            self.__token = data.get('token')
            self.userid = data.get('userId')

            # update header with the generated token
            self.__headers['Authorization'] = self.__token

    def reset_headers(self):
        """Reset the headers and params."""
        self.__headers = {
            'accept':        'application/json',
            'Content-Type':  'application/json',
            'Authorization':  self.__token
        }
        self.__params = {}

    def query(self, url, method='GET', extra_params=None, extra_headers=None, retry=3:
        """
        Returns a JSON object for an HTTP request.
        :param url: API URL
        :param method: Specify the method GET, POST or PUT (default=GET)
        :param extra_params: Dictionary to be appended on request.body
        :param extra_headers: Dictionary to be apppended on request.headers
        :param retry: Retry attempts for the query (default=3)
        """
        response = None
        self.reset_headers() # ensure the headers and params are reset to the bare minimum

        loop = 0
        while loop <= retry:

            # override request.body or request.headers dictionary
            params = self.__params
            if extra_params:
                params.update(extra_params)
            LOG.debug("Params: %s", params)

            headers = self.__headers
            if extra_headers:
                headers.update(extra_headers)
            LOG.debug("Headers: %s", headers)

            loop += 1
            LOG.debug("Querying %s on attempt: %s/%s", url, loop, retry)

            # define connection method
            request = None
            if method == 'GET':
                request = self.session.get(url, headers=headers, stream=stream)
            elif method == 'PUT':
                request = self.session.put(url, headers=headers, json=params)
            elif method == 'POST':
                request = self.session.post(url, headers=headers, json=params)
            else
                LOG.error("Invalid request method '%s'", method)
                return None

            if request and (request.status_code == 200):
                response = request.json()
                break # success!

        return response

    @property
    def sensors(self):
        """Return all sensors registered with the SensorPush account."""


        return None # FIXME

    @property
    def gateways(self):
        """Return all gateways registered with the SensorPush account."""
        return None # FIXME

    def update(self, update_sensors=False):
        """Refresh object."""
        self._authenticate()

        # update attributes on all sensors
        if update_sensors:
            url = LIST_SENSORS_ENDPOINT
            response = self.query(url)
            if not response or not isinstance(response, dict):
                return

            for sensor in self.sensors:
                for dev_info in response.get('data'):
                    if dev_info.get('deviceName') == sensor.name:
                        LOG.debug("Refreshing %s attributes", sensor.name)
                        sensor.attrs = dev_info
