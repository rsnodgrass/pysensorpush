"""Base Python Class file for SensorPush."""

import logging
import requests

from pysensorpush.sensor import SPSensor
from pysensorpush.const import ( LIST_SENSORS_ENDPOINT )

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
        self.cleanup_headers()
        url = LOGIN_ENDPOINT
        data = self.query(
            url,
            method='POST',
            extra_params={
                'email': self.__username,
                'password': self.__password
            })

        if isinstance(data, dict) and data.get('success'):
            data = data.get('data')
            self.authenticated = data.get('authenticated')
            self.country_code = data.get('countryCode')
            self.date_created = data.get('dateCreated')
            self.__token = data.get('token')
            self.userid = data.get('userId')

            # update header with the generated token
            self.__headers['Authorization'] = self.__token

    def reset_headers(self):
        """Reset the headers and params."""
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization':  self.__token
        }
        self.__headers = headers
        self.__params = {}

    def query(self,
              url,
              method='GET',
              extra_params=None,
              extra_headers=None,
              retry=3,
              raw=False,
              stream=False):
        """
        Return a JSON object or raw session.
        :param url: API URL
        :param method: Specify the method GET, POST or PUT. Default is GET.
        :param extra_params: Dictionary to be appended on request.body
        :param extra_headers: Dictionary to be apppended on request.headers
        :param retry: Attempts to retry a query. Default is 3.
        :param raw: Boolean if query() will return request object instead JSON.
        :param stream: Boolean if query() will return a stream object.
        """
        response = None
        loop = 0

        self.reset_headers() # ensure the headers and params are reset to the bare minimum

        while loop <= retry:

            # override request.body or request.headers dictionary
            if extra_params:
                params = self.__params
                params.update(extra_params)
            else:
                params = self.__params
            LOG.debug("Params: %s", params)

            if extra_headers:
                headers = self.__headers
                headers.update(extra_headers)
            else:
                headers = self.__headers
            LOG.debug("Headers: %s", headers)

            LOG.debug("Querying %s on attempt: %s/%s", url, loop, retry)
            loop += 1

            # define connection method
            req = None

            if method == 'GET':
                req = self.session.get(url, headers=headers, stream=stream)
            elif method == 'PUT':
                req = self.session.put(url, json=params, headers=headers)
            elif method == 'POST':
                req = self.session.post(url, json=params, headers=headers)

            if req and (req.status_code == 200):
                if raw:
                    LOG.debug("Required raw object.")
                    response = req
                else:
                    response = req.json()

                # leave if everything worked fine
                break

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
