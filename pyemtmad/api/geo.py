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

"""This file contains the endpoints for geo services.

See http://opendata.emtmadrid.es/Servicios-web/GEO
"""

from pyemtmad import types as emtype
from pyemtmad import util

class GeoApi(object):
    """Metaclass that contains the API methods for the geo endpoints."""

    def __init__(self, wrapper):
        """Initialization of the API module.

        Args:
            wrapper (Wrapper): Object that performs the requests to endpoints.
        """
        self._wrapper = wrapper
        self.make_request = self._wrapper.request_openbus

    def get_arrive_stop(self, **kwargs):
        """Obtain bus arrival info in target stop.

        Args:
            stop_number (int): Stop number to query.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Arrival]), or message string
            in case of error.
        """
        # Endpoint parameters
        params = {
            'idStop': kwargs.get('stop_number'),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_arrive_stop', **params)

        # Funny endpoint, no status code
        if not util.check_result(result, 'arrives'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'arrives')
        return True, [emtype.Arrival(**a) for a in values]

    def get_groups(self, **kwargs):
        """Obtain line types and details.

        Args:
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[GeoGroupItem]), or message
            string in case of error.
        """
        # Endpoint parameters
        params = {
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_groups', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.GeoGroupItem(**a) for a in values]

    def get_info_line(self, **kwargs):
        """Obtain basic information on a bus line on a given date.

        Args:
            day (int): Day of the month in format DD.
                The number is automatically padded if it only has one digit.
            month (int): Month number in format MM.
                The number is automatically padded if it only has one digit.
            year (int): Year number in format YYYY.
            lines (list[int] | int): Lines to query, may be empty to get
                all the lines.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Line]), or message string
            in case of error.
        """
        # Endpoint parameters
        select_date = '%02d/%02d/%d' % (
            kwargs.get('day', '01'),
            kwargs.get('month', '01'),
            kwargs.get('year', '1970')
        )

        params = {
            'fecha': select_date,
            'line': util.ints_to_string(kwargs.get('lines', [])),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_info_line', **params)

        # Funny endpoint, no status code
        if not util.check_result(result, 'Line'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'Line')
        return True, [emtype.Line(**a) for a in values]

    def get_info_line_extended(self, **kwargs):
        """Obtain extended information on a bus line on a given date.

        Args:
            day (int): Day of the month in format DD.
                The number is automatically padded if it only has one digit.
            month (int): Month number in format MM.
                The number is automatically padded if it only has one digit.
            year (int): Year number in format YYYY.
            lines (list[int] | int): Lines to query, may be empty to get
                all the lines.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Line]), or message string
            in case of error.
        """
        # Endpoint parameters
        select_date = '%02d/%02d/%d' % (
            kwargs.get('day', '01'),
            kwargs.get('month', '01'),
            kwargs.get('year', '1970')
        )

        params = {
            'fecha': select_date,
            'line': util.ints_to_string(kwargs.get('lines', [])),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_info_line_extended', **params)

        # Funny endpoint, no status code
        if not util.check_result(result, 'Line'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'Line')
        return True, [emtype.Line(**a) for a in values]

    def get_poi(self, **kwargs):
        """Obtain a list of POI in the given radius.

        Args:
            latitude (double): Latitude in decimal degrees.
            longitude (double): Longitude in decimal degrees.
            types (list[int] | int): POI IDs (or empty list to get all).
            radius (int): Radius (in meters) of the search.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Poi]), or message string
            in case of error.
        """
        # Endpoint parameters
        params = {
            'coordinateX': kwargs.get('longitude'),
            'coordinateY': kwargs.get('latitude'),
            'tipos': util.ints_to_string(kwargs.get('types')),
            'Radius': kwargs.get('radius'),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_poi', **params)

        # Funny endpoint, no status code
        if not util.check_result(result, 'poiList'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'poiList')
        return True, [emtype.Poi(**a) for a in values]

    def get_poi_types(self, **kwargs):
        """Obtain POI types.

        Args:
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[PoiType]), or message string
            in case of error.
        """
        # Endpoint parameters
        params = {
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_poi_types', **params)

        # Parse
        values = result.get('types', [])
        return True, [emtype.PoiType(**a) for a in values]

    def get_route_lines_route(self, **kwargs):
        """Obtain itinerary for one or more lines in the given date.

        Args:
            day (int): Day of the month in format DD.
                The number is automatically padded if it only has one digit.
            month (int): Month number in format MM.
                The number is automatically padded if it only has one digit.
            year (int): Year number in format YYYY.
            lines (list[int] | int): Lines to query, may be empty to get
                all the lines.

        Returns:
            Status boolean and parsed response (list[RouteLinesItem]), or message
            string in case of error.
        """
        # Endpoint parameters
        select_date = '%02d/%02d/%d' % (
            kwargs.get('day', '01'),
            kwargs.get('month', '01'),
            kwargs.get('year', '1970')
        )

        params = {
            'SelectDate': select_date,
            'Lines': util.ints_to_string(kwargs.get('lines', []))
        }

        # Request
        result = self.make_request('geo', 'get_route_lines_route', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.RouteLinesItem(**a) for a in values]

    def get_stops_from_stop(self, **kwargs):
        """Obtain a list of stops within the given radius of the specified stop.

        Args:
            stop_number (int): Number of the stop to query.
            radius (int): Radius (in meters) of the search.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Stop]), or message string
            in case of error.
        """
        # Endpoint parameters
        params = {
            'idStop': kwargs.get('stop_number'),
            'Radius': kwargs.get('radius'),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_stops_from_stop', **params)

        # Funny endpoint, no status code
        if not util.check_result(result, 'stops'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'stops')
        return True, [emtype.Stop(**a) for a in values]

    def get_stops_from_xy(self, **kwargs):
        """Obtain a list of stops around the given point.

        Arguments:
            latitude (double): Latitude in decimal degrees.
            longitude (double): Longitude in decimal degrees.
            radius (int): Radius (in meters) of the search.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Stop]), or message string
            in case of error.
        """
        # Endpoint parameters
        params = {
            'latitude': kwargs.get('latitude'),
            'longitude': kwargs.get('longitude'),
            'Radius': kwargs.get('radius'),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_stops_from_xy', **params)

        # Funny endpoint, no status code
        # No stop attribute could mean there are no stops in the zone specified
        if not util.check_result(result, 'stop'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'stop')
        return True, [emtype.Stop(**a) for a in values]

    def get_stops_line(self, **kwargs):
        """Obtain information on the stops of the given lines.

        Arguments:
            lines (list[int] | int): Lines to query, may be empty to get
                all the lines.
            direction (str): Optional, either *forward* or *backward*.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Stop]), or message string
            in case of error.
        """
        # Endpoint parameters
        params = {
            'line': util.ints_to_string(kwargs.get('lines', [])),
            'direction': util.direction_code(kwargs.get('direction', '')),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_stops_line', **params)

        # Funny endpoint, no status code
        # Only interested in 'stop'
        if not util.check_result(result, 'stop'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'stop')
        return True, [emtype.Stop(**a) for a in values]

    def get_street(self, **kwargs):
        """Obtain a list of nodes related to a location within a given radius.

        Not sure of its use, but...

        Args:
            street_name (str): Name of the street to search.
            street_number (int): Street number to search.
            radius (int): Radius (in meters) of the search.
            stops (int): Number of the stop to search.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Site]), or message string
            in case of error.
        """
        # Endpoint parameters
        params = {
            'description': kwargs.get('street_name'),
            'streetNumber': kwargs.get('street_number'),
            'Radius': kwargs.get('radius'),
            'Stops': kwargs.get('stops'),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_street', **params)

        # Funny endpoint, no status code
        if not util.check_result(result, 'site'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'site')
        return True, [emtype.Site(**a) for a in values]

    def get_street_from_xy(self, **kwargs):
        """Obtain a list of streets around the specified point.

        Args:
            latitude (double): Latitude in decimal degrees.
            longitude (double): Longitude in decimal degrees.
            radius (int): Radius (in meters) of the search.
            lang (str): Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[Street]), or message string
            in case of error.
        """
        # Endpoint parameters
        params = {
            'coordinateX': kwargs.get('longitude'),
            'coordinateY': kwargs.get('latitude'),
            'Radius': kwargs.get('radius'),
            'cultureInfo': util.language_code(kwargs.get('lang'))
        }

        # Request
        result = self.make_request('geo', 'get_street_from_xy', **params)

        # Funny endpoint, no status code
        if not util.check_result(result, 'site'):
            return False, 'UNKNOWN ERROR'

        # Parse
        values = util.response_list(result, 'site')
        return True, [emtype.Street(**a) for a in values]
