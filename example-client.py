#!/usr/local/bin/python3

import os
import sys
import logging

from pysensorpush import PySensorPush 

def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def main():
    #setup_logger()

    sensorpush = PySensorPush(os.getenv('SENSORPUSH_USER', None),
                              os.getenv('SENSORPUSH_PASSWORD', None))

    print("Gateways = %s", sensorpush.gateways)

    print("Sensors = %s", sensorpush.sensors)

    print("Samples = %s", sensorpush.samples)

if __name__ == "__main__":
    main()
