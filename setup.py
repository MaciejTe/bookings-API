""" Installation script for Booking REST API.

    Usage:
        python setup.py install
        python setup.py develop (for production)
"""
import re

from setuptools import setup
from setuptools import find_packages


def get_latest_version():
    """ Get latest application version from the CHANGELOG.md file.

        Returns:
            latest_version(str): latest version of the application,
                                 or ??.??.?? in case of wrong formatted file.
    """
    changelog_file_path = 'CHANGELOG.md'
    with open(changelog_file_path, 'r') as change_file:
        changes = change_file.readlines()

    ver_regex = r'(?P<ver>\d{2}.\d{2}.\d{2})\s+\(\d+/\d+/\d+\)\s*\Z'
    versions = [re.match(ver_regex, line).groupdict()['ver']
                for line in changes if re.match(ver_regex, line)]

    versions_splitted = [tuple(ver.split('.')) for ver in versions]
    versions_splitted.sort(key=lambda x: (x[0], x[1], x[2]))
    try:
        latest_version = '.'.join(versions_splitted.pop())
    except IndexError:
        latest_version = '??.??.??'

    return latest_version


def get_requirements():
    """ Get all Python modules required by application to be installed.

        Returns:
            modules(list): list of Python modules
    """
    requirements_file_path = 'requirements.txt'
    with open(requirements_file_path, 'r') as req_file:
        modules = req_file.readlines()
    modules = [module.strip() for module in modules if module.strip()]
    return modules


setup(
    name='Bookings API',
    version=get_latest_version(),
    description='REST API for booking purposes',
    author='Maciej Tomczuk',
    author_email='tomczukmaciej@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(),
    # entry_points={
    #     'console_scripts': [
    #         'pdg = src.shell:run'
    #     ]
    # }
)