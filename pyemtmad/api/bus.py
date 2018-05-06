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

"""This file contains the endpoints for bus services.

See http://opendata.emtmadrid.es/Servicios-web/BUS
"""

from pyemtmad import types as emtype
from pyemtmad import util

class BusApi(object):
    """Metaclass that contains the API methods for the bus endpoints."""

    def __init__(self, wrapper):
        """Initialization of the API module.

        Args:
            wrapper (Wrapper): Object that performs the requests to endpoints.
        """
        self._wrapper = wrapper
        self.make_request = self._wrapper.request_openbus

    def get_calendar(self, **kwargs):
        """Obtain EMT calendar for a range of dates.

        Args:
            start_day (int): Starting day of the month in format DD.
                The number is automatically padded if it only has one digit.
            start_month (int): Starting month number in format MM.
                The number is automatically padded if it only has one digit.
            start_year (int): Starting year number in format YYYY.
            end_day (int): Ending day of the month in format DD.
                The number is automatically padded if it only has one digit.
            end_month (int): Ending month number in format MM.
                The number is automatically padded if it only has one digit.
            end_year (int): Ending year number in format YYYY.

        Returns:
            Status boolean and parsed response (list[CalendarItem]), or message
            string in case of error.
        """
        # Endpoint parameters
        start_date = util.date_string(
            kwargs.get('start_day', '01'),
            kwargs.get('start_month', '01'),
            kwargs.get('start_year', '1970')
        )

        end_date = util.date_string(
            kwargs.get('end_day', '01'),
            kwargs.get('end_month', '01'),
            kwargs.get('end_year', '1970')
        )

        params = {'SelectDateBegin': start_date, 'SelectDateEnd': end_date}

        # Request
        result = self.make_request('bus', 'get_calendar', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.CalendarItem(**a) for a in values]

    def get_groups(self, **kwargs):
        """Obtain line types and details.

        Args:
            lang(str):  Language code (*es* or *en*).

        Returns:
            Status boolean and parsed response (list[BusGroupItem]), or message
            string in case of error.
        """
        # Endpoint parameters
        params = {'cultureInfo': util.language_code(kwargs.get('lang'))}

        # Request
        result = self.make_request('bus', 'get_groups', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.BusGroupItem(**a) for a in values]

    def get_list_lines(self, **kwargs):
        """Obtain lines with description and group.

        Args:
            day (int): Day of the month in format DD.
                The number is automatically padded if it only has one digit.
            month (int): Month number in format MM.
                The number is automatically padded if it only has one digit.
            year (int): Year number in format YYYY.
            lines (list[int] | int): Lines to query, may be empty to get
                all the lines.

        Returns:
            Status boolean and parsed response (list[ListLineInfo]), or message
            string in case of error.
        """
        # Endpoint parameters
        select_date = util.date_string(
            kwargs.get('day', '01'),
            kwargs.get('month', '01'),
            kwargs.get('year', '1970')
        )

        # Lines separated by |
        lines = util.ints_to_string(kwargs.get('lines', []))

        params = {'SelectDate': select_date, 'Lines': lines}

        # Request
        result = self.make_request('bus', 'get_list_lines', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.ListLineInfo(**a) for a in values]

    def get_nodes_lines(self, **kwargs):
        """Obtain stop IDs, coordinates and line information.

        Args:
            nodes (list[int] | int): nodes to query, may be empty to get
                all nodes.

        Returns:
            Status boolean and parsed response (list[NodeLinesItem]), or message
            string in case of error.
        """
        # Endpoint parameters
        params = {'Nodes': util.ints_to_string(kwargs.get('nodes', []))}

        # Request
        result = self.make_request('bus', 'get_nodes_lines', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.NodeLinesItem(**a) for a in values]

    def get_route_lines(self, **kwargs):
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
        select_date = util.date_string(
            kwargs.get('day', '01'),
            kwargs.get('month', '01'),
            kwargs.get('year', '1970')
        )

        lines = util.ints_to_string(kwargs.get('lines', []))

        params = {'SelectDate': select_date, 'Lines': lines}

        # Request
        result = self.make_request('bus', 'get_route_lines', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.RouteLinesItem(**a) for a in values]



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
        select_date = util.date_string(
            kwargs.get('day', '01'),
            kwargs.get('month', '01'),
            kwargs.get('year', '1970')
        )

        lines = util.ints_to_string(kwargs.get('lines', []))

        params = {'SelectDate': select_date, 'Lines': lines}

        # Request
        result = self.make_request('bus', 'get_route_lines_route', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.RouteLinesItem(**a) for a in values]

    def get_times_lines(self, **kwargs):
        """Obtain current line times for the given lines.

        Args:
            day (int): Day of the month in format DD.
                The number is automatically padded if it only has one digit.
            month (int): Month number in format MM.
                The number is automatically padded if it only has one digit.
            year (int): Year number in format YYYY.
            lines (list[int] | int): Lines to query, may be empty to get
                all the lines.

        Returns:
            Status boolean and parsed response (list[TimesLinesItem]), or message
            string in case of error.
        """
        # Endpoint parameters
        select_date = util.date_string(
            kwargs.get('day', '01'),
            kwargs.get('month', '01'),
            kwargs.get('year', '1970')
        )

        lines = util.ints_to_string(kwargs.get('lines', []))

        params = {'SelectDate': select_date, 'Lines': lines}

        # Request
        result = self.make_request('bus', 'get_times_lines', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.TimesLinesItem(**a) for a in values]

    def get_timetable_lines(self, **kwargs):
        """Obtain information on lines for a travel.

        Args:
            day (int): Day of the month in format DD.
                The number is automatically padded if it only has one digit.
            month (int): Month number in format MM.
                The number is automatically padded if it only has one digit.
            year (int): Year number in format YYYY.
            lines (list[int] | int): Lines to query, may be empty to get
                all the lines.

        Returns:
            Status boolean and parsed response (list[TimetableLinesItem]),
            or message string in case of error.
        """
        # Endpoint parameters
        select_date = util.date_string(
            kwargs.get('day', '01'),
            kwargs.get('month', '01'),
            kwargs.get('year', '1970')
        )

        lines = util.ints_to_string(kwargs.get('lines', []))

        # Request
        params = {'SelectDate': select_date, 'Lines': lines}
        result = self.make_request('bus', 'get_timetable_lines', **params)

        if not util.check_result(result):
            return False, result.get('resultDescription', 'UNKNOWN ERROR')

        # Parse
        values = util.response_list(result, 'resultValues')
        return True, [emtype.TimetableLinesItem(**a) for a in values]
