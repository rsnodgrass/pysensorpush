"""
A Python wrapper for the Foobot air quality sensor API.
Allows for data to be queried in three ways:
  1. Get the latest sample from the foobot
  2. Get data from an interval
  3. Get data from a time span
"""

import requests

__version__ = '0.2'
BASE_URL = 'https://api.Foobot.io/v2'


class Foobot:
    """Class for authentication and getting foobot devices."""

    def __init__(self, apikey, username, password):
        """Authenticate the username and password."""
        self.username = username
        self.password = password
        self.session = requests.Session()

        self.auth_header = {'Accept': 'application/json;charset=UTF-8',
                            'X-API-KEY-TOKEN': apikey}

        token = self.login()
        if token is None:
            raise ValueError("Provided username or password is not valid.")

        self.auth_header['X-AUTH-TOKEN'] = token

    def login(self):
        """Log into a foobot device."""
        url = '{base}/user/{user}/login/'.format(base=BASE_URL,
                                                 user=self.username)
        req = self.session.get(url,
                               auth=(self.username, self.password),
                               headers=self.auth_header)
        return req.headers['X-AUTH-TOKEN'] if req.text == "true" else None

    def devices(self):
        """Get list of foobot devices owned by logged in user."""
        url = '{base}/owner/{user}/device/'.format(base=BASE_URL,
                                                   user=self.username)
        req = self.session.get(url, headers=self.auth_header)

        def create_device(device):
            """Helper to create a FoobotDevice based on a dictionary."""
            return FoobotDevice(auth_header=self.auth_header,
                                user_id=device['userId'],
                                uuid=device['uuid'],
                                name=device['name'],
                                mac=device['mac'])

        return [create_device(device) for device in req.json()]


# pylint: disable=too-many-arguments
class FoobotDevice:
    """Represents a foobot device."""

    def __init__(self, auth_header, user_id, uuid, name, mac):
        """Create a foobot device instance used for getting data samples."""
        self.auth_header = auth_header
        self.user_id = user_id
        self.uuid = uuid
        self.name = name
        self.mac = mac
        self.session = requests.Session()

    def latest(self):
        """Get latest sample from foobot device."""
        url = '{base}/device/{uuid}/datapoint/{period}/last/{sampling}/'
        url = url.format(base=BASE_URL,
                         uuid=self.uuid,
                         period=0,
                         sampling=0)
        req = self.session.get(url, headers=self.auth_header)
        return req.json()

    def data_period(self, period, sampling):
        """Get a specified period of data samples."""
        url = '{base}/device/{uuid}/datapoint/{period}/last/{sampling}/'
        url = url.format(base=BASE_URL,
                         uuid=self.uuid,
                         period=period,
                         sampling=sampling)

        req = self.session.get(url, headers=self.auth_header)
        return req.json()

    def data_range(self, start, end, sampling):
        """Get a specified range of data samples."""
        url = '{base}/device/{uuid}/datapoint/{start}/{end}/{sampling}/'
        url = url.format(base=BASE_URL,
                         uuid=self.uuid,
                         start=start,
                         end=end,
                         sampling=sampling)

        req = self.session.get(url, headers=self.auth_header)
        return req.json()
