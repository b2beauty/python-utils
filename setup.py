# -*- coding: utf-8 -*-
try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from navegg_utils import __version__

setup(
    name='NaveggUtils',
    version=__version__,
    author='Felipe Arenhardt Tomaz',
    author_email='felipa.a.tomaz@gmail.com',
    packages=['navegg_utils'],
    scripts=[],
    url='http://www.navegg.com/',
    license='LICENSE.txt',
    description='Navegg Utils - Python Library.',
    long_description=open('README.txt').read(),
    install_requires=[
        'pika >= 0.9.13',
        'MySQL-python >= 1.2',
        'simplejson >= 3.3',
        'selenium',
    ],
)
