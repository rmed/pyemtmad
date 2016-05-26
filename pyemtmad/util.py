# -*- coding: utf-8 -*-
# pyemtmad, EMT API wrapper - https://github.com/rmed/pyemtmad
# Copyright (C) 2016  Rafael Medina García <rafamedgar@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
This file contains some utility functions used in the API interface.
"""

import ssl
import six
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager


class ParkingAdapter(HTTPAdapter):
    """Custom HTTP adapter for parking API, as it uses TLSv1."""

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)


def check_result(data, key=''):
    """Check the result of an API response.

    Ideally, this should be done by checking that the value of the ``resultCode``
    attribute is 0, but there are endpoints that simply do not follow this rule.

    Args:
        data (dict): Response obtained from the API endpoint.
        key (string): Key to check for existence in the dict.

    Returns:
        bool: True if result was correct, False otherwise.
    """
    if not isinstance(data, dict):
        return False

    if key:
        if key in data:
            return True

        return False

    if 'resultCode' in data.keys():
        # OpenBus
        return True if data.get('resultCode', -1) == 0 else False

    elif 'code' in data.keys():
        # Parking
        return True if data.get('code', -1) == 0 else False

    return False

def date_string(day, month, year):
    """Build a date string using the provided day, month, year numbers.

    Automatically adds a leading zero to ``day`` and ``month`` if they only have
    one digit.

    Args:
        day (int): Day number.
        month(int): Month number.
        year(int): Year number.

    Returns:
        str: Date in the format *DD/MM/YYYY*.
    """
    return '%02d/%02d/%d' % (day, month, year)

def datetime_string(day, month, year, hour, minute):
    """Build a date string using the provided day, month, year numbers.

    Automatically adds a leading zero to ``day`` and ``month`` if they only have
    one digit.

    Args:
        day (int): Day number.
        month(int): Month number.
        year(int): Year number.
        hour (int): Hour of the day in 24h format.
        minute (int): Minute of the hour.

    Returns:
        str: Date in the format *YYYY-MM-DDThh:mm:ss*.
    """
    # Overflow
    if hour < 0 or hour > 23: hour = 0
    if minute < 0 or minute > 60: minute = 0

    return '%d-%02d-%02dT%02d:%02d:00' % (year, month, day, hour, minute)

def direction_code(direction):
    """Obtain the integer code of a direction string.

    Args:
        direction (str): *forward* or *backward*

    Returns:
        int: direction code
    """
    if direction == 'backward':
        return 2

    return 1

def ints_to_string(ints):
    """Convert a list of integers to a *|* separated string.

    Args:
        ints (list[int]|int): List of integer items to convert or single
            integer to convert.

    Returns:
        str: Formatted string
    """
    if not isinstance(ints, list):
        return six.u(str(ints))

    return '|'.join(six.u(str(l)) for l in ints)

def language_code(code):
    """Generate the ``cultureInfo`` language code for the API.

    Available codes are *EN* (default) and *ES*.

    Args:
        code (str): Two-character language code.

    Returns:
        str: Language code in the format accepted by the API.
    """
    if not code or code == 'es':
        return 'ES'

    return 'EN'

def response_list(data, key):
    """Obtain the relevant response data in a list.

    If the response does not already contain the result in a list, a new one
    will be created to ease iteration in the parser methods.

    Args:
        data (dict): API response.
        key (str): Attribute of the response that contains the result values.

    Returns:
        List of response items (usually dict) or None if the key is not present.
    """
    if key not in data:
        return None

    if isinstance(data[key], list):
        return data[key]

    else:
        return [data[key],]
