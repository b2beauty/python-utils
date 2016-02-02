# -*- coding: utf-8 -*-
from distutils.core import setup

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from agendabeleza_utils import __version__

setup(
    name='AgendabelezaUtils',
    version=__version__,
    author='Salvador chavez',
    author_email='salvachz@gmail.com',
    packages=['agendabeleza_utils'],
    scripts=[],
    url='https://beautydate.com.br/',
    license='LICENSE.txt',
    description='Agendabeleza Utils - Python Library.',
    long_description=open('README.txt').read(),
    install_requires=[
        'pika >= 0.9.13',
        'MySQL-python >= 1.2',
        'simplejson >= 3.3',
	'python-dateutil >= =2.2',
    ],
)
