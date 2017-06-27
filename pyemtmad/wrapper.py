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

"""This file contains the API URL and endpoints for EMT.

See http://opendata.emtmadrid.es/Servicios-web
"""

import requests
from pyemtmad.api.bus import BusApi
from pyemtmad.api.geo import GeoApi
from pyemtmad.api.parking import ParkingApi
from pyemtmad.util import ParkingAdapter

# Custom request for parking API
_parking_req = requests.Session()
_parking_req.mount('https://', ParkingAdapter())

# API URLs
URL_OPENBUS = 'https://openbus.emtmadrid.es:9443/emt-proxy-server/last/'
URL_PARKING = 'https://servicios.emtmadrid.es:8443/infoParking/infoParking.svc/json/'


# JSON endpoints
ENDPOINTS_BUS = {
    'get_calendar'           : 'bus/GetCalendar.php',
    'get_groups'             : 'bus/GetGroups.php',
    'get_list_lines'         : 'bus/GetListLines.php',
    'get_nodes_lines'        : 'bus/GetNodesLines.php',
    'get_route_lines'        : 'bus/GetRouteLines.php',
    'get_route_lines_route'  : 'bus/GetRouteLinesRoute.php',
    'get_times_lines'        : 'bus/GetTimesLines.php',
    'get_timetable_lines'    : 'bus/GetTimeTableLines.php'
}

ENDPOINTS_GEO = {
    'get_arrive_stop'        : 'geo/GetArriveStop.php',
    'get_arrive_client'      : 'geo/GetArriveClient.php',
    'get_groups'             : 'geo/GetGroups.php',
    'get_info_line'          : 'geo/GetInfoLine.php',
    'get_info_line_extended' : 'geo/GetInfoLineExtend.php',
    'get_poi'                : 'geo/GetPointsOfInterest.php',
    'get_poi_types'          : 'geo/GetPointsOfInterestTypes.php',
    'get_route_lines_route'  : 'geo/GetRouteLinesRoute.php',
    'get_stops_from_stop'    : 'geo/GetStopsFromStop.php',
    'get_stops_from_xy'      : 'geo/GetStopsFromXY.php',
    'get_stops_line'         : 'geo/GetStopsLine.php',
    'get_street'             : 'geo/GetStreet.php',
    'get_street_from_xy'     : 'geo/GetStreetFromXY.php'
}

ENDPOINTS_PARKING = {
    'detail_parking'          : 'detailParking/{id_client},{passkey}',
    'detail_poi'              : 'detailPOI/{id_client},{passkey}',
    'icon_description'        : 'iconDescription/{id_client},{passkey}',
    'info_parking_poi'        : 'infoParkingPoi/{id_client},{passkey}',
    'list_features'           : 'listFeatures/{id_client},{passkey}',
    'list_parking'            : 'listFeatures/{id_client},{passkey},{lang}',
    'list_street_poi_parking' : 'listStreetPoisParking/{id_client},{passkey},{address},{lang}',
    'list_types_poi'          : 'listTypesPOIs/{id_client},{passkey},{lang}'
}


class Wrapper(object):
    """Interface for the JSON API of the EMT services."""

    def __init__(self, emt_id='', emt_pass=''):
        """Initialize the interface attributes.

        Initialization may also be performed at a later point by manually
        calling the ``initialize()`` method.

        Args:
            emt_id (str): ID given by the server upon registration
            emt_pass (str): Token given by the server upon registration
        """
        if emt_id and emt_pass:
            self.initialize(emt_id, emt_pass)

    def initialize(self, emt_id, emt_pass):
        """Manual initialization of the interface attributes.

        This is useful when the interface must be declare but initialized later
        on with parsed configuration values.

        Args:
            emt_id (str): ID given by the server upon registration
            emt_pass (str): Token given by the server upon registration
        """
        self._emt_id = emt_id
        self._emt_pass = emt_pass

        # Initialize modules
        self.bus = BusApi(self)
        self.geo = GeoApi(self)
        self.parking = ParkingApi(self)

    def request_openbus(self, service, endpoint, **kwargs):
        """Make a request to the given endpoint of the ``openbus`` server.

        This returns the plain JSON (dict) response which can then be parsed
        using one of the implemented types.

        Args:
            service (str): Service to fetch ('bus' or 'geo').
            endpoint (str): Endpoint to send the request to.
                This string corresponds to the key in the ``ENDPOINTS`` dict.
            **kwargs: Request arguments.

        Returns:
            Obtained response (dict) or None if the endpoint was not found.
        """
        if service == 'bus':
            endpoints = ENDPOINTS_BUS

        elif service == 'geo':
            endpoints = ENDPOINTS_GEO

        else:
            # Unknown service
            return None

        if endpoint not in endpoints:
            # Unknown endpoint
            return None

        url = URL_OPENBUS + endpoints[endpoint]

        # Append credentials to request
        kwargs['idClient'] = self._emt_id
        kwargs['passKey'] = self._emt_pass

        # SSL verification fails...
        # return requests.post(url, data=kwargs, verify=False).json()
        return requests.post(url, data=kwargs, verify=True).json()

    def request_parking(self, endpoint, url_args={}, **kwargs):
        """Make a request to the given endpoint of the ``parking`` server.

        This returns the plain JSON (dict) response which can then be parsed
        using one of the implemented types.

        Args:
            endpoint (str): Endpoint to send the request to.
                This string corresponds to the key in the ``ENDPOINTS`` dict.
            url_args (dict): Dictionary for URL string replacements.
            **kwargs: Request arguments.

        Returns:
            Obtained response (dict) or None if the endpoint was not found.
        """
        if endpoint not in ENDPOINTS_PARKING:
            # Unknown endpoint
            return None

        url = URL_OPENBUS + ENDPOINTS_PARKING[endpoint]

        # Append additional info to URL
        lang = url_args.get('lang', 'ES')
        address = url_args.get('address', '')

        url = url.format(
            id_client=self._emt_id,
            passkey=self._emt_pass,
            address=address,
            lang=lang
        )

        # This server uses TLSv1
        return _parking_req.post(url, data=kwargs).json()
