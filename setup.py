#!/usr/bin/env python

import os
import sys
from pathlib import Path

import setuptools

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

long_descriptions = Path('README.md').read_text()

setuptools.setup(
    name='pysensorpush',
    version='0.1.8',
    packages=['pysensorpush'],
    description='Python interface for the SensorPush API',
    url='https://github.com/rsnodgrass/pysensorpush',
    author='Ryan Snodgrass',
    author_email='rsnodgrass@gmail.com',
    license='Apache Software License',
    install_requires=['requests>=2.0'],
    keywords=['sensorpush', 'home automation', 'humidity', 'temperature'],
    zip_safe=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
)
