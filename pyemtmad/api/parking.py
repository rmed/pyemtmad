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

"""This file contains the endpoints for parking services.

See https://servicios.emtmadrid.es:8443/InfoParking/InfoParking.svc/json/help
"""

from pyemtmad import types as emtype
from pyemtmad import util

class ParkingApi(object):
    """Metaclass that contains the API methods for the parking endpoints."""

    def __init__(self, wrapper):
        """Initialization of the API module.

        Args:
            wrapper (Wrapper): Object that performs the requests to endpoints.
        """
        self._wrapper = wrapper
        self.make_request = self._wrapper.request_parking

    def detail_parking(self, **kwargs):
        """Obtain detailed info of a given parking.

        Args:
            lang (str):  Language code (*es* or *en*).
            day (int): Day of the month in format DD.
                The number is automatically padded if it only has one digit.
            month (int): Month number in format MM.
                The number is automatically padded if it only has one digit.
            year (int): Year number in format YYYY.
            hour (int): Hour of the day in format hh.
                The number is automatically padded if it only has one digit.
            minute (int): Minute of the hour in format mm.
                The number is automatically padded if it only has one digit.
            parking (int): ID of the parking to query.
            family (str): Family code of the parking (3 chars).

        Returns:
            Status boolean and parsed response (list[ParkingDetails]), or message
            string in case of error.
        """
        # Endpoint parameters
        date = util.datetime_string(
            kwargs.get('day', 1),
            kwargs.get('month', 1),
            kwargs.get('year', 1970),
            kwargs.get('hour', 0),
            kwargs.get('minute', 0)
        )

        params = {
            'language': util.language_code(kwargs.get('lang')),
            'publicData': True,
            'date': date,
            'id': kwargs.get('parking'),
            'family': kwargs.get('family')
        }

        # Request
        result = self.make_request('detail_parking', {}, **params)

        if not util.check_result(result):
            return False, result.get('message', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'Data')
        return True, [emtype.ParkingDetails(**a) for a in values]

    def detail_poi(self, **kwargs):
        """Obtain detailed info of a given POI.

        Args:
            family (str): Family code of the POI (3 chars).
            lang (str): Language code (*es* or *en*).
            id (int): Optional, ID of the POI to query. Passing value -1 will
                result in information from all POIs.

        Returns:
            Status boolean and parsed response (list[PoiDetails]), or
            message string in case of error.
        """
        # Endpoint parameters
        params = {
            'language': util.language_code(kwargs.get('lang')),
            'family': kwargs.get('family')
        }

        if kwargs.get('id'):
            params['id'] = kwargs['id']

        # Request
        result = self.make_request('detail_poi', {}, **params)

        if not util.check_result(result):
            return False, result.get('message', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'Data')
        return True, [emtype.PoiDetails(**a) for a in values]

    def icon_description(self, **kwargs):
        """Obtain a list of elements that have an associated icon.

        Args:
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[IconDescription]), or
            message string in case of error.
        """
        # Endpoint parameters
        params = {'language': util.language_code(kwargs.get('lang'))}

        # Request
        result = self.make_request('icon_description', {}, **params)

        if not util.check_result(result):
            return False, result.get('message', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'Data')
        return True, [emtype.IconDescription(**a) for a in values]

    def info_parking_poi(self, **kwargs):
        """Obtain generic information on POIs and parkings.

        This returns a list of elements in a given radius from the coordinates.

        Args:
            radius (int): Radius of the search (in meters).
            latitude (double): Latitude in decimal degrees.
            longitude (double): Longitude in decimal degrees.
            lang (str): Language code (*es* or *en*).
            day (int): Day of the month in format DD.
                The number is automatically padded if it only has one digit.
            month (int): Month number in format MM.
                The number is automatically padded if it only has one digit.
            year (int): Year number in format YYYY.
            hour (int): Hour of the day in format hh.
                The number is automatically padded if it only has one digit.
            minute (int): Minute of the hour in format mm.
                The number is automatically padded if it only has one digit.
            poi_info (list[tuple]): List of tuples with the format
                ``(list[family], type, category)`` to query. Check the API
                documentation.
            min_free (list[int]): Number of free spaces to check. Must have the
                same length of ``poi_info``.
            field_codes (list[tuple]): List of tuples with the format
                ``(list[codes], name)``. Check the API documentation.

        Returns:
            Status boolean and parsed response (list[InfoParkingPoi]), or
            message string in case of error.
        """
        # Endpoint parameters
        date = util.datetime_string(
            kwargs.get('day', 1),
            kwargs.get('month', 1),
            kwargs.get('year', 1970),
            kwargs.get('hour', 0),
            kwargs.get('minute', 0)
        )

        family_categories = []
        for element in kwargs.get('poi_info', []):
            family_categories.append({
                'poiCategory': {
                    'lstCategoryTypes': element[0]
                    },
                'poiFamily': element[1],
                'poiType': element[2]
            })

        field_codes = []
        for element in kwargs.get('field_codes', []):
            field_codes.append({
                'codes': {
                    'lstCodes': element[0]
                    },
                'nameField': element[1]
            })

        params = {
            'TFamilyTTypeTCategory': {
                'lstFamilyTypeCategory': family_categories
            },
            'coordinate': {
                'latitude': str(kwargs.get('latitude', '0.0')),
                'longitude': str(kwargs.get('longitude', '0.0'))
            },
            'dateTimeUse': date,
            'language': util.language_code(kwargs.get('lang')),
            'minimumPlacesAvailable': {
                'lstminimumPlacesAvailable': kwargs.get('min_free', [])
            },
            'nameFieldCodes': {
                'lstNameFieldCodes': field_codes
            },
            'radius': str(kwargs.get('radius', '0'))
        }

        # Request
        result = self.make_request('info_parking_poi', {}, **params)

        if not util.check_result(result):
            return False, result.get('message', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'Data')
        return True, [emtype.InfoParkingPoi(**a) for a in values]

    def list_features(self, **kwargs):
        """Obtain a list of parkings.

        Args:
            lang (str):  Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Parking]), or message
            string in case of error.
        """
        # Endpoint parameters
        params = {
            'language': util.language_code(kwargs.get('lang')),
            'publicData': True
        }

        # Request
        result = self.make_request('list_features', {}, **params)

        if not util.check_result(result):
            return False, result.get('message', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'Data')
        return True, [emtype.ParkingFeature(**a) for a in values]

    def list_parking(self, **kwargs):
        """Obtain a list of parkings.

        Args:
            lang (str):  Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Parking]), or message
            string in case of error.
        """
        # Endpoint parameters
        url_args = {'lang': util.language_code(kwargs.get('lang'))}

        # Request
        result = self.make_request('list_parking', url_args)

        if not util.check_result(result):
            return False, result.get('message', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'Data')
        return True, [emtype.Parking(**a) for a in values]

    def list_street_poi_parking(self, **kwargs):
        """Obtain a list of addresses and POIs.

        This endpoint uses an address to perform the search

        Args:
            lang (str): Language code (*es* or *en*).
            address (str): Address in which to perform the search.

        Returns:
            Status boolean and parsed response (list[ParkingPoi]), or message
            string in case of error.
        """
        # Endpoint parameters
        url_args = {
            'language': util.language_code(kwargs.get('lang')),
            'address': kwargs.get('address', '')
        }

        # Request
        result = self.make_request('list_street_poi_parking', url_args)

        if not util.check_result(result):
            return False, result.get('message', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'Data')
        return True, [emtype.ParkingPoi(**a) for a in values]

    def list_types_poi(self, **kwargs):
        """Obtain a list of families, types and categories of POI.

        Args:
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[ParkingPoiType]), or message
            string in case of error.
        """
        # Endpoint parameters
        url_args = {'language': util.language_code(kwargs.get('lang'))}

        # Request
        result = self.make_request('list_poi_types', url_args)

        if not util.check_result(result):
            return False, result.get('message', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'Data')
        return True, [emtype.ParkingPoiType(**a) for a in values]
