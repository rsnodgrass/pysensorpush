#!/usr/bin/python3

import os
import sys
import pprint
import logging

from pysensorpush import PySensorPush


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def main():
    user = os.getenv("SENSORPUSH_USER", None)
    password = os.getenv("SENSORPUSH_PASSWORD", None)

    if (user == None) or (password == None):
        print(
            "ERROR! Must define env variables SENSORPUSH_USER and SENSORPUSH_PASSWORD"
        )
        raise SystemExit

    # setup_logger()
    pp = pprint.PrettyPrinter(indent=2)

    sensorpush = PySensorPush(user, password)

    print("--Gateways--")
    pp.pprint(sensorpush.gateways)

    print("\n--Sensors--")
    pp.pprint(sensorpush.sensors)

    print("\n--Samples--")
    pp.pprint(sensorpush.samples)


if __name__ == "__main__":
    main()
