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

"""This file contains type definitions for the data returned by the API."""

import datetime

WEEK_DAYS = {
    'L': 'Monday',
    'M': 'Tuesday',
    'X': 'Wednesday',
    'J': 'Thursday',
    'V': 'Friday',
    'S': 'Saturday',
    'D': 'Sunday'
}

DAY_TYPES = {
    'LA'        : 'Labour',
    'V'         : 'Friday',
    'SA'        : 'Saturday',
    'FE'        : 'Festive',
    'LABORABLE' : 'Labour',
    'SABADO'    : 'Saturday',
    'FESTIVO'   : 'Festive'
}

SEC_DETAILS = {
    10: 'forward_stop',
    19: 'forward_vertex',
    20: 'backward_stop',
    29: 'backward_vertex'
}

POI_TYPES = {
    1 : 'cars',
    10: 'shopping',
    11: 'tourism',
    12: 'metro',
    13: 'light rail',
    14: 'interchange',
    15: 'transport places I',
    16: 'transport places II',
    17: 'RENFE',
    2 : 'services',
    3 : 'education',
    4 : 'leisure',
    5 : 'financial entities',
    6 : 'hospitals',
    7 : 'parkings',
    8 : 'recreation centers',
    9 : 'restaurants'
}

PARKING_POI_TYPES = {
    'Zona'    : 'zone',
    'Poi'     : 'poi',
    'Parking' : 'parking'
}


class Arrival(object):
    """
    Attributes:
        stop_id (int): Stop ID.
        line_id (string): Line ID.
        is_header (bool): Whether or not the stop is header of the line.
        destination (string): Destination of the bus.
        bus_id (int): Bus ID.
        time_left (int): Seconds remaining until bus arrives.
            If this value is >= 999999, then 20+ minutes remain.
        distance (int): distance of the bus in meters.
        longitude (double): Longitude of the bus in decimal degrees
        latitude (double): Latitude of the bus in decimal degrees
        position_type (string): Real or estimate position

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.stop_id = kwargs.get('stopId')
        self.line_id = kwargs.get('lineId')
        self.is_head = False if kwargs.get('isHead') == 'False' else True
        self.destination = kwargs.get('destination')
        self.bus_id = int(kwargs.get('busId', '-1'))
        self.time_left = kwargs.get('busTimeLeft')
        self.distance = kwargs.get('busDistance')
        self.longitude = kwargs.get('longitude')
        self.latitude = kwargs.get('latitude')

        pos_type = kwargs.get('busPositionType')
        if pos_type == 0:
            self.position_type = 'real'

        elif pos_type == 1:
            self.position_type = 'estimate'


        self._json = kwargs


class BusGroupItem(object):
    """
    Attributes:
        id (int): Group ID.
        description (string): Group description.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = int(kwargs.get('groupId'))
        self.description = kwargs.get('groupDescription').strip()

        self._json = kwargs


class CalendarItem(object):
    """
    Attributes:
        date (string): Date in DD/MM/YYYY H:mm:ss format.
        day_type (string): Day type. May be:
            - labour (LA)
            - friday (F)
            - saturday (SA)
            - festive (FE)
        strike (boolean): Whether there is strike on this day or not.
        day_of_week (string): Day of the week (in english) obtained from
            single character Spanish representation.
        week (int): Week number.
        month (int): Month number.
        trimester (int): Trimester number.
        quarter (int): Quarter number.
        semester (int): Semester number.
        year (int): Year number.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.date = kwargs.get('date', '').replace('\\', '').strip()
        self.week = kwargs.get('week')
        self.month = kwargs.get('month')
        self.trimester = kwargs.get('trimester')
        self.quarter = kwargs.get('quarter')
        self.semester = kwargs.get('semester')
        self.year = kwargs.get('year')

        self.day_type = DAY_TYPES.get(kwargs.get('typeDay'), 'Labour')

        on_strike = kwargs.get('strike', 'N')
        if on_strike == 'Y':
            self.strike = True

        elif on_strike == 'N':
            self.strike = False

        day_week = kwargs.get('dayOfWeek')
        self.day_of_week = WEEK_DAYS.get(day_week, 'Monday')

        self._json = kwargs


class DayType(object):
    """
    Attributes:
        day_type (string): Day type. May be:
            - labour (LA)
            - friday (F)
            - saturday (SA)
            - festive (FE)
        dir_forward (Direction): Forward line direction details.
        dir_backward (Direction): Backward line direction details.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.day_type = DAY_TYPES.get(kwargs.get('dayTypeId'), 'Labour')
        self.dir_forward = Direction(**kwargs.get('direction1'))
        self.dir_backward = Direction(**kwargs.get('direction2'))

        self._json = kwargs


class Direction(object):
    """
    Attributes:
        start_time (string): Starting time in HH:mm.
        end_time (string): Ending time in HH:mm.
        minimum_frequency (int): Minimum frequency of buses in minutes.
        maximum_frequency (int): Maximum frequency of buses in minutes.
        frequency_description (string): Human readable description of the
            frequency (in extended call).

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.start_time = kwargs.get('startTime')
        self.end_time = kwargs.get('endTime')
        self.minimum_frequency = kwargs.get('minimumFrequency')
        self.maximum_frequency = kwargs.get('maximumFrequency')
        self.frequency_description = kwargs.get('frequencyDescription', '') \
                .replace('\\', '').strip()

        self._json = kwargs


class GeoGroupItem(object):
    """
    Attributes:
        id (int): group ID.
        subgroup (int): subgroup ID.
        start_date (int): starting date timestamp.
        end_date (int): ending date timestamp.
        description (string): description text.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('groupId')
        self.subgroup = kwargs.get('subGroupId')
        self.start_date = kwargs.get('startDate')
        self.end_date = kwargs.get('endDate')
        self.description = kwargs.get('description')

        self._json = kwargs


class IconDescription(object):
    """
    Attributes:
        classification (str): Localized name of the group of the icon.
        classification_spanish (str): Original name of the group of the icon.
        description (str): Description of the referenced element.
        icon_name (str): Name of the element.
        url_icon (str): URL to the icon.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.classification = kwargs.get('classificationTranslated')
        self.classification_spanish = kwargs.get('classification')
        self.description = kwargs.get('description')
        self.icon_name = kwargs.get('iconName')
        self.url_icon = kwargs.get('urlIcon')

        self._json = kwargs


class InfoParkingPoi(object):
    """
    Attributes:
        id (int): Parking or POI ID. They are identified with (family, id).
        name (str): Parking or POI name.
        address (str): Parking or POI address.
        type (str): Parking or POI type.
        type_code (str): Parking or POI type code.
        administrative_area (str): Administrative area in which the parking or
            POI is located. This is usually 'Madrid'.
        area_code (int): Postal code of the parking or POI.
        category (str): Parking or POI category name.
        category_code(str): Parking or POI category code.
        country (str): Country in which the parking or POI is located ('Spain').
        email (str): Public email of the POI.
        family (str): Family of the parking or POI.
        family_code (str): Unique code of the family.
        fax (str): Public fax of the POI.
        url_icon (str): URL to the icon representing the parking or POI.
        state (str): State in which the parking or POI is located.
        telephone (str): Public telephone of the POI.
        town (str): Town in which the parking or POI is located.
        latitude (double): Latitude of the parking or POI in decimal degrees.
        longitude (double): Longitude of the parking or POI in decimal degrees.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.type = kwargs.get('type')
        self.type_code = kwargs.get('typeCode')
        self.administrative_area = kwargs.get('administrativeArea')
        self.area_code = int(kwargs.get('areaCode', '-1'))
        self.category = kwargs.get('category')
        self.category_code = kwargs.get('categoryCode')
        self.country = kwargs.get('country')
        self.email = kwargs.get('email')
        self.family = kwargs.get('familyName')
        self.family_code = kwargs.get('family')
        self.fax = kwargs.get('fax')
        self.url_icon = kwargs.get('icon')
        self.state = kwargs.get('state')
        self.telephone = kwargs.get('telephone')
        self.town = kwargs.get('town')
        self.latitude = float(kwargs.get('latitude', '0.0'))
        self.longitude = float(kwargs.get('longitude', '0.0'))

        self._json = kwargs

class Line(object):
    """
    Attributes:
        id (int): Line ID.
        label (string): Line label.
        date (string): Date in which information was updated (dd/mm/YYYY).
        header_a (string): Name of the end of the line A.
        header_b (string): Name of the end of the line B.
        incidents (int): Number of incidents in the line.
        day_types (list[DayType]) - list of day types for this line.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('lineId')
        self.label = kwargs.get('label')
        self.header_a = kwargs.get('headerA')
        self.header_b = kwargs.get('headerB')
        self.incidents = kwargs.get('incidents')

        # Extended version returns a timestamp
        if 'date' in kwargs.keys():
            # Extended
            self.date = datetime.datetime.fromtimestamp(
                kwargs.get('date', 0) / 1e3)

        elif 'string' in kwargs.keys():
            # Basic
            self.date = kwargs.get('string', '').replace('\\', '').strip()

        self.day_types = [DayType(**a) for a in kwargs.get('dayType', [])]

        self._json = kwargs


class LineInfo(object):
    """
    Attributes:
        day_type (string): Day type. May be:
            - labour (LA)
            - friday (F)
            - saturday (SA)
            - festive (FE)
        line (int): Line number.
        label (string): Label of the line.
        header_a (string): Name of the end of the line A.
        header_b (string): Name of the end of the line B.
        direction (string): Direction of the line.
        start_time (string): Time in which the line starts service (HH:mm).
        end_time (string): Time in which the line ends service (HH:mm).
        minimum_frequency (int): minimum frequency of buses in minutes.
        maximum_frequency (int):maximum frequency of buses in minutes.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.line = int(kwargs.get('name'))
        self.label = kwargs.get('label')
        self.header_a = kwargs.get('headerA')
        self.header_b = kwargs.get('headerB')
        self.start_time = kwargs.get('startTime')
        self.end_time = kwargs.get('stopTime')
        self.minimum_frequency = int(kwargs.get('minimumFrequency', '-1'))
        self.maximum_frequency = int(kwargs.get('maximumFrequency', '-1'))

        self.day_type = DAY_TYPES.get(kwargs.get('typeDay'), 'Labour')

        direction = kwargs.get('direction', 'A')
        if direction == 'A':
            self.direction = 'forward'
        elif direction == 'B':
            self.direction = 'backward'

        self._json = kwargs


class ListLineInfo(object):
    """
    Attributes:
        group (int): Group number.
        start_date (string): Date in which line started service (DD/MM/YYYY).
        end_date (string): Date in which line ended service (DD/MM/YYYY).
        line (int): Line number.
        label (string): Label of the line.
        header_a (string): Name of the end of the line A.
        header_b (string): Name of the end of the line B.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.group = int(kwargs.get('groupNumber', '0'))
        self.start_date = kwargs.get('dateFirst', '').replace('\\', '').strip()
        self.end_date = kwargs.get('dateEnd', '').replace('\\', '').strip()
        self.line = int(kwargs.get('line', '0'))
        self.label = kwargs.get('label')
        self.header_a = kwargs.get('nameA')
        self.header_b = kwargs.get('nameB')

        self._json = kwargs


class NodeLinesItem(object):
    """
    Attributes:

        id (int): Node ID.
        name (string): Node name.
        lines (list[tuple]): Line ID and direction.
        latitude (double): Latitude of the node in decimal degrees.
        longitude (double): Longitude of the node in decimal degrees.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('node')
        self.name = kwargs.get('name')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')

        lines = kwargs.get('lines')
        self.lines = []

        for line in lines:
            if line:
                elements = line.replace('\\', '').strip().split('/')
                print(elements)
                # 1 = forward, 2 = backward
                direction = 'forward' if elements[1] == '1' else 'backward'
                self.lines.append((int(elements[0]), direction))

        self._json = kwargs


class Parking(object):
    """
    Attributes:
        id (int): Parking ID. Parkings are identified with (family, id).
        name (str): Parking name.
        address (str): Parking address.
        type (str): Parking type.
        administrative_area (str): Administrative area in which the parking is
            located. This is usually 'Madrid'.
        area_code (int): Postal code of the parking.
        category (str): Parking category code.
        country (str): Country in which the parking is located ('Spain').
        family (str): Family of the parking.
        family_code (str): Unique code of the family.
        nickname (str): Nickname of the parking.
        state (str): State in which the parking is located.
        town (str): Town in which the parking is located.
        latitude (double): Latitude of the parking in decimal degrees.
        longitude (double): Longitude of the parking in decimal degrees.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.type = kwargs.get('type')
        self.administrative_area = kwargs.get('administrativeArea')
        self.area_code = int(kwargs.get('areaCode', '-1'))
        self.category = kwargs.get('category')
        self.country = kwargs.get('country')
        self.family = kwargs.get('family')
        self.family_code = kwargs.get('familyCode')
        self.nickname = kwargs.get('nickName')
        self.state = kwargs.get('state')
        self.town = kwargs.get('town')
        self.latitude = float(kwargs.get('latitude', '0.0'))
        self.longitude = float(kwargs.get('longitude', '0.0'))

        self._json = kwargs


class ParkingAccess(object):
    """
    Attributes:
        name (str): Name of the access.
        address (str): Address where the access is located.
        code (str): ID code of the access.
        url_icon (str): URL to the icon representing the access.
        latitude (double): Latitude of the access in decimal degrees.
        longitude (double): Longitude of the access in decimal degrees.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.code = kwargs.get('code')
        self.url_icon = kwargs.get('url_icon')
        self.latitude = float(kwargs.get('latitude', '0.0'))
        self.longitude = float(kwargs.get('longitude', '0.0'))

        self._json = kwargs

class ParkingDetails(object):
    """
    Attributes:
        id (int): ID of the parking.
        name (str): Name of the parking.
        schedule (str): Time in which the parking is open.
        address (str): Parking address.
        administrative_area (str): Administrative area in which the parking is
            located. This is usually 'Madrid'.
        area_code (str): Postal code of the parking.
        category (str): Name of the parking category.
        category_code (str): Parking category code.
        type (str): Parking type.
        type_code (str): Parking type code.
        country (str): Country in which the parking is located ('Spain').
        url_icon (str): URL to the icon representing this feature, if any.
        nickname (str): Nickname of the parking.
        state (str): State in which the parking is located.
        town (str): Town in which the parking is located.
        latitude (double): Latitude of the parking in decimal degrees.
        longitude (double): Longitude of the parking in decimal degrees.

        accesses (list[ParkingAccess]): List of accesses to this parking.
        features (list[ParkingFeature]): List of features of this parking.
        occupation (list[ParkingOccupation]): List of occupation details.
        rates (list[ParkingRate]): List of parking rates.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        general = kwargs.get('general', {})

        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.schedule = kwargs.get('schedule')
        self.address = general.get('address')
        self.administrative_area = general.get('administrativeArea')
        self.area_code = general.get('areaCode')
        self.category = general.get('category')
        self.category_code = general.get('categoryCode')
        self.type = general.get('type')
        self.type_code = general.get('typeCode')
        self.country = general.get('country')
        self.family = kwargs.get('family')
        self.family_code = kwargs.get('familyCode')
        self.nickname = general.get('nickName')
        self.state = general.get('state')
        self.town = general.get('town')
        self.latitude = float(general.get('latitude', '0.0'))
        self.longitude = float(general.get('longitude', '0.0'))

        accesses = kwargs.get('lstAccess', [])
        features = kwargs.get('lstFeatures', [])
        occupation = kwargs.get('lstOccupation', [])
        rates = kwargs.get('lstRates', [])

        self.accesses = [ParkingAccess(**a) for a in accesses]
        self.features = [ParkingFeature(**a) for a in features]
        self.occupation = [ParkingOccupation(**a) for a in occupation]
        self.rates = [ParkingRate(**a) for a in rates]

        self._json = kwargs


class ParkingFeature(object):
    """
    Attributes:
        name (str): Name of the feature.
        code (str): 3-char ID code of the feature.
        content (str): Content of the feature, if any.
        description (str): Description of the feature, if any.
        field (str): Localized name of the group the feature belongs to.
        field_spanish (str): Original name of the group the feature belongs to.
        url_icon (str): URL to the icon representing this feature, if any.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.code = kwargs.get('nameCode')
        self.description = kwargs.get('description')
        self.field = kwargs.get('nameFieldTranslated')
        self.field_spanish = kwargs.get('nameField')
        self.url_icon = kwargs.get('urlIcon')

        self._json = kwargs


class ParkingOccupation(object):
    """
    Attributes:
        type (str): Type of slot.
        code (str): 3-char ID code of the feature.
        free (int): Number of free slots.
        moment (str): Moment in which the data was updated.
        renewal_index (double): Renewal index of the parking.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.type = kwargs.get('name')
        self.code = kwargs.get('code')
        self.free = kwargs.get('free')
        self.moment = kwargs.get('moment')
        self.renewal_index = kwargs.get('renewal_index')

        self._json = kwargs


class ParkingPoi(object):
    """
    Attributes:
        id (int): Parking ID. Parkings are identified with (family, id).
        name (str): Parking name.
        address (str): Parking address.
        address_number (str): Street number of the POI (only for addresses).
        type (str): Element type. Possible types are:
            - zone
            - poi
            - parking
        administrative_area (str): Administrative area in which the parking is
            located. This is usually 'Madrid'.
        area_code (int): Postal code of the parking.
        category (str): Parking category code.
        country (str): Country in which the parking is located ('Spain').
        email (str): Email of the POI (if any).
        family (str): Family of the parking.
        family_code (str): Unique code of the family.
        fax (str): Fax number of the POI (if any).
        url_icon (str): URL to the icon representing this POI, if any.
        nickname (str): Nickname of the parking.
        state (str): State in which the parking is located.
        telephone (str): Phone number.
        town (str): Town in which the parking is located.
        latitude (double): Latitude of the parking in decimal degrees.
        longitude (double): Longitude of the parking in decimal degrees.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.address = kwargs.get('address')
        self.address_number = kwargs.get('addressNumber')
        self.type = PARKING_POI_TYPES.get(kwargs.get('type', ''), 'zone')
        self.administrative_area = kwargs.get('administrativeArea')
        self.area_code = int(kwargs.get('areaCode', '-1'))
        self.category = kwargs.get('category')
        self.country = kwargs.get('country')
        self.email = kwargs.get('email')
        self.family = kwargs.get('family')
        self.family_code = kwargs.get('familyCode')
        self.fax = kwargs.get('fax')
        self.url_icon = kwargs.get('neutralIcon')
        self.nickname = kwargs.get('nickName')
        self.state = kwargs.get('state')
        self.telephone = kwargs.get('telephone')
        self.town = kwargs.get('town')
        self.latitude = float(kwargs.get('latitude', '0.0'))
        self.longitude = float(kwargs.get('longitude', '0.0'))

        self._json = kwargs


class ParkingPoiType(object):
    """
    Attributes:
        name (str): Name of the POI type.
        code (str): Code of the POI type.
        category (str): Name of the POI category.
        category_code (str): Code of the POI category.
        family (str): Name of the POI family.
        family_code (str): Unique code of the family.
        url_icon (str): URL to the icon representing this POI, if any.

        _json (dict): Original API response.
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('type')
        self.code = kwargs.get('typeCode')
        self.category = kwargs.get('category')
        self.category_code = kwargs.get('categoryCode')
        self.family = kwargs.get('family')
        self.family_code = kwargs.get('familyCode')
        self.url_icon = kwargs.get('neutralIcon')

        self._json = kwargs


class ParkingRate(object):
    """
    Attributes:
        description (str): Rate description.
        start_minutes (int): Start minutes of the stay.
        end_minutes (int): End minutes of the stay.
        type (str): Type of rate (minutes, max, etc.)
        rate (double): Amount to pay given the rate type
        schedule_start (str): Starting time of the rate.
        schedule_end (str): End time of the rate.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.start_minutes = kwargs.get('minutesStayInitiation')
        self.end_minutes = kwargs.get('minutesStayEnd')
        self.type = kwargs.get('periodPricing')
        self.rate = kwargs.get('rate')
        self.schedule_start = kwargs.get('scheduleInitial')
        self.schedule_end = kwargs.get('scheduleEnd')

        self._json = kwargs


class Poi(object):
    """
    Attributes:
        id (int): POI ID.
        poi_type (string): POI type.
        name (string): POI name.
        address (string): POI address.
        street_number (int): Street number of the POI.
        phone_number (string): Phone number of the POI (if any).
        latitude (double): latitude in decimal degrees.
        longitude (double): longitude in decimal degrees.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        attrs = kwargs.get('attributes', {})
        self.id = attrs.get('poiId')
        self.poi_type = POI_TYPES.get(attrs.get('poiType', -1), '')
        self.name = attrs.get('name')
        self.address = attrs.get('address')
        self.street_number = attrs.get('streetNumber')
        self.phone_number = attrs.get('phoneNumber')
        self.latitude = attrs.get('latitude')
        self.longitude = attrs.get('longitude')

        self._json = kwargs


class PoiDetails(object):
    """
    Attributes:
        id (int): ID of the POI.
        name (str): Localized name of the POI.
        name_spanish (str): Original POI name.
        description (str): Description of the POI.
        schedule (str): Time in which the POI is open.
        address (str): Parking address.
        administrative_area (str): Administrative area in which the POI is
            located. This is usually 'Madrid'.
        area_code (str): Postal code of the POI.
        category (str): Name of the POI category.
        category_code (str): POI category code.
        type (str): POI type.
        type_code (str): POI type code.
        country (str): Country in which the parking is located ('Spain').
        email (str): Email of the POI, if any.
        telephone (str): Public phone number of the POI, if any.
        fax (str): Public fax of the POI, if any.
        url_icon (str): URL to the icon representing this feature, if any.
        state (str): State in which the parking is located.
        town (str): Town in which the parking is located.
        services_payment (str): Payment services.
        web (str): Website of the POI, if any.
        latitude (double): Latitude of the parking in decimal degrees.
        longitude (double): Longitude of the parking in decimal degrees.

        images (list[PoiImage]): List of images attached to this POI.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        info = kwargs.get('poiDetailInfo', {})

        self.id = kwargs.get('id')
        self.name = info.get('nameTranslated')
        self.name_spanish = kwargs.get('name')
        self.description = info.get('description')
        self.schedule = info.get('schedule')
        self.address = kwargs.get('address')
        self.administrative_area = kwargs.get('administrativeArea')
        self.area_code = kwargs.get('areaCode')
        self.category = kwargs.get('category')
        self.category_code = kwargs.get('categoryCode')
        self.type = kwargs.get('type')
        self.type_code = kwargs.get('typeCode')
        self.country = kwargs.get('country')
        self.email = kwargs.get('email')
        self.telephone = kwargs.get('telephone')
        self.fax = kwargs.get('fax')
        self.url_icon = kwargs.get('icon')
        self.state = kwargs.get('state')
        self.town = kwargs.get('town')
        self.services_payment = info.get('servicesPayment')
        self.web = info.get('web')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')

        detail_images = kwargs.get('poiDetailImages', [])
        self.images = [PoiImage(**a) for a in detail_images]

        self._json = kwargs


class PoiImage(object):
    """
    Attributes:
        description (str): Description of the image, if any.
        url (str): URL to the image.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.description = kwargs.get('description')
        self.url = kwargs.get('urlImage')

        self._json = kwargs


class PoiType(object):
    """
    Attributes:
        id (int): Type ID.
        name (string): Type name.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        attrs = kwargs.get('attributes', {})

        self.id = attrs.get('type')
        self.name = attrs.get('name')

        self._json = kwargs


class RouteLinesItem(object):
    """
    Attributes:
        id (int): Node ID.
        line (int): Line to which the node belongs.
        node_type (string): Node type. May be:
            - forward_stop (10)
            - forward_vertex (19)
            - backward_stop (20)
            - backward_vertex (29)
        distance_orig (double): Distance to origin in meters.
        distance_prev (double): Distance to previous stop in meters.
        name (string): Name of the stop.
        latitude (double): Latitude in decimal degrees.
        longitude (double): Longitude in decimal degrees.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get('node')
        self.line = kwargs.get('line')
        self.distance_orig = kwargs.get('distance')
        self.distance_prev = kwargs.get('distancePreviousStop')
        self.name = kwargs.get('name')
        self.latitude = kwargs.get('latitude')
        self.longitude = kwargs.get('longitude')

        sec_detail = kwargs.get('secDetail')
        self.node_type = SEC_DETAILS.get(sec_detail, 'forward_stop')

        self._json = kwargs


class Site(object):
    """
    Attributes:
        id (int): Site ID.
        site_type (string): Site type. May be:
            - street
            - poi
        name (string): Name of the site.
        longitude (double): longitude of the site in decimal degrees.
        latitude (double): latitude of the site in decimal degrees.

        street_type (string): Type of the street (avenue, street, etc.).
        number_type (string): Type of street numbering.
        street_number (int): Street number.
        zip_code (int): Street zip code.

        poi_type (string): Type of POI.
        poi_address (string): Address of the POI.
        poi_street_number (int): Street number of the POI.
        poi_direction (string): Direction of the POI.
        poi_phone_number (string): Phone number of the POI.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = int(kwargs.get('siteId', '0'))
        self.name = kwargs.get('description')
        self.longitude = kwargs.get('longitude')
        self.latitude = kwargs.get('latitude')

        site_type = kwargs.get('site_type', '')
        if site_type == 'C':
            self.site_type = 'street'
        elif site_type == 'P':
            self.site_type = 'poi'

        # Street
        self.street_type = kwargs.get('streetType')
        self.number_type = kwargs.get('numberType')
        self.street_number = int(kwargs.get('streetNumber', '-1'))
        self.zip_code = int(kwargs.get('zipCode', '-1'))

        # POI
        self.poi_type = POI_TYPES.get(int(kwargs.get('poiType', '-1')), '')
        self.poi_address = kwargs.get('poiAddress')
        self.poi_street_number = int(kwargs.get('poiStreetNumber', '-1'))
        self.poi_direction = kwargs.get('poiDirection')
        self.poi_phone_number = kwargs.get('poiPhoneNumber')

        self._json = kwargs


class Stop(object):
    """
    Attributes:
        id (int): Stop ID.
        name (string): Stop name.
        address (string): Postal address of the stop.
        longitude (double): Longitude of the stop in decimal degrees.
        latitude (double): Latitude of the stop in decimal degrees.
        lines (list[LineInfo]): Lines that stop here.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.id = int(kwargs.get('stopId'))
        self.name = kwargs.get('name')
        self.address = kwargs.get('postalAddress')
        self.longitude = kwargs.get('longitude')
        self.latitude = kwargs.get('latitude')

        if 'line' in kwargs:
            if isinstance(kwargs.get('line'), list):
                # Several lines
                self.lines = [LineInfo(**a) for a in kwargs.get('line')]

            else:
                # Single line
                self.lines = [LineInfo(**kwargs.get('line'))]

        self._json = kwargs


class Street(object):
    """
    Attributes:
        name (string): Name of the street.
        street_type (string): Type of street.
        street_number (int): Number of the street building.
        latitude (double): Latitude in decimal degrees.
        longitude (double): Longitude in decimal degrees.

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        attrs = kwargs.get('attributes', {})
        self.name = attrs.get('streetName')
        self.street_type = attrs.get('streetType')
        self.street_number = int(attrs.get('number', '-1'))
        self.latitude = attrs.get('latitude')
        self.longitude = attrs.get('longitude')

        self._json = kwargs


class TimesLinesItem(object):
    """
    Attributes:
        start_date (string): Date in which line started service (DD/MM/YYYY).
        end_date (string): Date in which line ended service (DD/MM/YYYY).
        line (int): Line number.
        day_type (string): Day type. May be:
            - labour (LA)
            - friday (F)
            - saturday (SA)
            - festive (FE)
        first_forward (string): Date and time of first bus forward (A-B).
            (DD/MM/YYYY H:mm:ss)
        first_backward (string): Date and time of first bus backward (B-A).
            (DD/MM/YYYY H:mm:ss)
        last_forward (string): Date and time of last bus forward (A-B).
            (DD/MM/YYYY H:mm:ss)
        last_backward (string): Date and time of last bus backward (B-A).
            (DD/MM/YYYY H:mm:ss)

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.start_date = kwargs.get('dateFirst', '').replace('\\', '').strip()
        self.end_date = kwargs.get('dateEnd', '').replace('\\', '').strip()
        self.line = int(kwargs.get('line', '0'))
        self.first_forward = kwargs.get('timeFirstA').replace('\\', '').strip()
        self.first_backward = kwargs.get('timeFirstB').replace('\\', '').strip()
        self.last_forward = kwargs.get('timeEndA').replace('\\', '').strip()
        self.last_backward = kwargs.get('timeEndB').replace('\\', '').strip()

        self.day_type = DAY_TYPES.get(kwargs.get('typeId'), 'Labour')

        self._json = kwargs


class TimetableLinesItem(object):
    """
    Attributes:
        date (string): Date for the timetable (DD/MM/YYYY).
        day_type (string): Day type. May be:
            - labour (LA)
            - friday (F)
            - saturday (SA)
            - festive (FE)
        line (int): Line number
        direction (string) - forward or backward
        trip (int) - trip number.
        start_time (string): Starting time (HH:mm:ss).
        end_time (string): Ending time (HH:mm:ss).

        _json (dict): Original API response.
    """

    def __init__(self, **kwargs):
        self.date = kwargs.get('date', '').replace('\\', '').strip()
        self.line = int(kwargs.get('line', '0'))
        self.start_time = kwargs.get('timeFirst', '').replace('\\', '').strip()
        self.end_time = kwargs.get('timeEnd', '').replace('\\', '').strip()

        self.day_type = DAY_TYPES.get(kwargs.get('typeDay'), 'Labour')

        direction = int(kwargs.get('direction'))
        if direction == 1:
            self.direction = 'forward'

        elif direction == 2:
            self.direction = 'backward'

        self._json = kwargs
