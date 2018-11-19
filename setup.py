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
    version='0.0.1',
    description=get_long_description(current_directory),

    packages=[],
    include_package_data=True
)
