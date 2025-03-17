"""Python class for SensorPush sensor."""

import logging

LOG = logging.getLogger(__name__)


def assert_is_dict(var):
    """Assert variable is from the type dictionary."""
    if var is None or not isinstance(var, dict):
        return {}
    return var


class SPSensor:
    """SensorPush sensor implementation."""

    def __init__(self, name, attrs, sensorpush_session):
        """Initialize SensorPush sensor object.
        :param name: sensor name
        :param attrs: sensor attributes
        :param sensorpush_session: PySensorPush shared session
        """
        self.name = name
        self._attrs = attrs
        self._session = sensorpush_session

        # make sure self._attrs is a dict
        self._attrs = assert_is_dict(self._attrs)

    def __repr__(self):
        """Representation string of object."""
        return '<{}: {}>'.format(self.__class__.__name__, self.name)

    @property
    def attrs(self):
        """Return sensor attributes."""
        return self._attrs

    @attrs.setter
    def attrs(self, value):
        """Override sensors attributes."""
        self._attrs = value

    @property
    def temperature(self):
        """Returns temperature from latest sample."""
        return None

    @property
    def humidity(self):
        """Returns humididy from latest sample."""
        return None

    def update(self):
        """Update object properties."""
        self._attrs = self._session.refresh_attributes(self.name)
        self._attrs = assert_is_dict(self._attrs)

        # force associated gateway to update
        if self.gateway:
            self.gateway.update()
