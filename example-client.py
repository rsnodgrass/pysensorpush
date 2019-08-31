#!/usr/local/bin/python3

import os
import sys
import logging

from pysensorpush import PySensorPush 

def main():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    sensorpush = PySensorPush(os.getenv('SENSORPUSH_USER', None),
                              os.getenv('SENSORPUSH_PASSWORD', None))
    print(sensorpush.sensors)
    print(sensorpush.gateways)

if __name__ == "__main__":
    main()