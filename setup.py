"""
Setup

"""

from setuptools import setup
from os import path

from setup.common import (
    get_long_description
)

current_directory = path.abspath(path.dirname(__file__))

setup(
    name='amazon-review-scraper',
    version='0.0.4',
    description=get_long_description(current_directory),

    dependency_links=[
        'https://github.com/dateutil/dateutil.git'
    ],

    install_requires=[
        'python-dateutil',
        'fake_useragent',
        'lxml',
        'requests'
    ],

    packages=[
        'scraper.core',
        'scraper.product',
        'scraper.request',
        'scraper.search',
    ],
    include_package_data=True
)
