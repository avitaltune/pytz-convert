#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  @copyright 2016 TUNE, Inc. (http://www.tune.com)
#  @namespace tune_mv_integration
"""
Helpers: Timezone Utils.
"""

import collections
import math
import datetime as dt
import dateutil.tz as dtz
import pytz
# from pprintpp import pprint

TIMEZONE_NAMES_PREFERRED = [
    'Pacific/Midway',  # -1100
    'US/Hawaii',  # -1000
    'US/Alaska',  # -0900
    'US/Pacific',  # -0800
    'US/Mountain',  # -0700
    'US/Central',  # -0600
    'US/Eastern',  # -0500
    'Atlantic/Bermuda',  # -0400
    'Atlantic/Stanley',  # -0300
    'Atlantic/South_Georgia',  # -0200
    'Atlantic/Azores',  # -0100
    'UTC',  # +0000
    'Europe/Berlin',  # +0100
    'Asia/Jerusalem',  # +0200
    'Asia/Qatar',  # +0300
    'Asia/Dubai',  # +0400
    'Asia/Samarkand',  # +0500
    'Asia/Dhaka',  # +0600
    'Asia/Bangkok',  # +0700
    'Asia/Hong_Kong',  # +0800
    'Asia/Tokyo',  # +0900
    'Pacific/Guam',  # +1000
    'Australia/Sydney',  # +1100
    'Pacific/Fiji',  # +1200
    'Pacific/Auckland',  # +1300
    'Pacific/Honolulu',
    'America/Anchorage',
    'America/Los_Angeles',
    'America/Denver',
    'America/Chicago',
    'America/New_York',
    'Europe/Moscow',
    'Asia/Kolkata'
]


def convert_tz_abbrev_to_tz_names(tz_abbrev):
    """Convert timezone abbreviation to timezone names.
    """
    if not tz_abbrev:
        raise ValueError("Parameter 'tz_abbrev' is undefined.")

    if tz_abbrev in ['GMT', 'UTC']:
        return tz_abbrev

    tzones = collections.defaultdict(list)
    for name in pytz.common_timezones:
        tzone = pytz.timezone(name)

        # pylint: disable=protected-access
        try:
            for utcoffset, dstoffset, tzabbrev in tzone._transition_info:
                tzones[tzabbrev].append(name)
        except AttributeError:
            now = dt.datetime.now()
            now = tzone.localize(now)
            tzones[now.strftime('%Z')].append(name)
        # pylint: enable=protected-access

    for abbrev, names in tzones.items():
        tzones[abbrev] = list(set(names))

    if tz_abbrev not in tzones:
        raise ValueError("Invalid 'tz_abbrev': {tz_abbrev}".format(tz_abbrev=tz_abbrev))

    return tzones[tz_abbrev]


def convert_tz_abbrev_to_tz_offset(tz_abbrev):
    """Convert timezone abbreviation to timezone offset.

    Args:
        tz_abbrev:

    Returns:

    """
    if not tz_abbrev:
        raise ValueError("Parameter 'tz_abbrev' is undefined.")

    for _tz_name in pytz.common_timezones:
        _timezone = dtz.gettz(_tz_name)
        now = dt.datetime.now(_timezone)

        _tz_abbrev = now.strftime('%Z')
        if tz_abbrev != _tz_abbrev:
            continue

        _tz_offset = now.strftime('%z')
        return _tz_offset

    raise ValueError("Invalid 'tz_abbrev': {tz_abbrev}".format(tz_abbrev=tz_abbrev))


def convert_tz_offset_and_date_to_tz_name(tz_offset, str_date, str_country_code=None):
    """Convert Timezone offset + Date to Timezone Name

    Args:
        tz_offset:
        str_date:
        str_country_code:

    Returns:

    """
    if not str_date:
        raise ValueError("Parameter 'str_date' is undefined.")
    if not tz_offset:
        raise ValueError("Parameter 'tz_offset' is undefined.")

    tz_names = []

    for tz_name in pytz.common_timezones:
        _tz_offset = convert_tz_name_to_date_tz_offset(tz_name=tz_name, str_date=str_date)

        if tz_offset != _tz_offset:
            continue

        tz_names.append(tz_name)

    if not tz_names or len(tz_names) == 0:
        raise ValueError("Invalid 'tz_offset': {}".format(tz_offset))

    if str_country_code and str_country_code in pytz.country_timezones:
        tz_names_country = []
        for tz_name in tz_names:
            if tz_name in pytz.country_timezones[str_country_code]:
                tz_names_country.append(tz_name)

        if tz_names_country and len(tz_names_country) > 0:
            tz_names_country_preferred = \
                sorted(set(tz_names_country).intersection(TIMEZONE_NAMES_PREFERRED))

            if tz_names_country_preferred and len(tz_names_country_preferred) > 0:
                return tz_names_country_preferred[0]

            return tz_names_country[0]
        else:
            return None

    tz_names_preferred = \
        sorted(set(tz_names).intersection(TIMEZONE_NAMES_PREFERRED))

    if tz_names_preferred and len(tz_names_preferred) > 0:
        return tz_names_preferred[0]

    return tz_names[0]


def convert_tz_offset_to_now_tz_abbrev(tz_offset):
    """Convert timezone offset to current date's timezone abbreviation.

    Args:
        tz_offset:

    Returns:

    """
    if not tz_offset:
        raise ValueError("Parameter 'tz_offset' is undefined.")

    tz_abbrevs = []

    for _tz_name in pytz.common_timezones:
        _timezone = dtz.gettz(_tz_name)
        now = dt.datetime.now(_timezone)

        _tz_offset = now.strftime('%z')
        if tz_offset != _tz_offset:
            continue

        _tz_abbrev = now.strftime('%Z')
        tz_abbrevs.append(_tz_abbrev)

    if not tz_abbrevs or len(tz_abbrevs) == 0:
        raise ValueError("Invalid 'tz_offset': {}".format(tz_offset))

    return sorted(set(tz_abbrevs))


def convert_tz_name_to_now_tz_offset(tz_name):
    """Convert timezone name to current date's timezone offset.

    Args:
        tz_name:

    Returns:

    """

    if not tz_name:
        raise ValueError("Parameter 'tz_name' is undefined.")

    _timezone = dtz.gettz(tz_name)
    now = dt.datetime.now(_timezone)

    _tz_offset = now.strftime('%z')
    return _tz_offset


def convert_tz_name_to_date_tz_offset(tz_name, str_date):
    """Convert timezone name to provided date's timezone abbreviation.

    Args:
        tz_name:
        date:

    Returns:

    """
    return pytz.timezone(tz_name).localize(dt.datetime.strptime(str_date, "%Y-%m-%d")).strftime('%z')


def convert_tz_name_to_now_tz_abbrev(tz_name):
    """Convert timezone name to current timezone abbreviation.

    Args:
        tz_name:

    Returns:

    """

    if not tz_name:
        raise ValueError("Parameter 'tz_name' is undefined.")

    tz_file = dtz.gettz(tz_name)
    _tz_now = dt.datetime.now(tz=tz_file)
    _tz_abbrev = _tz_now.strftime('%Z')
    return _tz_abbrev


def convert_tz_name_to_date_tz_abbrev(tz_name, str_date):
    """Convert timezone name to date's timezone abbreviation.

    Args:
        tz_name:
        str_date:

    Returns:

    """

    if not tz_name:
        raise ValueError("Parameter 'tz_name' is undefined.")

    tz_file = dtz.gettz(tz_name)

    _date = dt.datetime.strptime(str_date, "%Y-%m-%d")
    _tz_date = dt.datetime(year=_date.year, month=_date.month, day=_date.day, tzinfo=tz_file)
    _tz_abbrev = _tz_date.strftime('%Z')
    return _tz_abbrev


def convert_tz_name_to_date_tz_offset(tz_name, str_date):
    """Convert timezone name to provided date's timezone abbreviation.
    Args:
        tz_name:
        date:
    Returns:
    """
    return pytz.timezone(tz_name).localize(dt.datetime.strptime(str_date, "%Y-%m-%d")).strftime('%z')


def convert_tz_offset_to_tz_hours(tz_offset):
    """Convert timezone offset to hours.

    Args:
        tz_offset:

    Returns:

    """
    int_offset = int(tz_offset)
    int_hours = int(int_offset / 100)
    int_minutes = int(int_offset % 100)

    tz_hours = int_hours + (int_minutes / 60)

    return tz_hours


def convert_tz_hours_to_tz_offset(tz_hours):
    """Convert Timezone hours into Timezone offset.

    Args:
        tz_hours:

    Returns:

    """
    _tz_signed = tz_hours < 0
    if _tz_signed:
        tz_hours *= -1

    frac, whole = math.modf(tz_hours)

    int_hours = int(whole)
    int_minutes = int(frac * 60)

    tz_offset = str(int_hours).zfill(2) + str(int_minutes).zfill(2)
    if _tz_signed:
        tz_offset = "-" + tz_offset
    else:
        tz_offset = "+" + tz_offset

    return tz_offset


def convert_tz_offset_to_tz_minutes(tz_offset):
    """Convert timezone offset to minutes.

    Args:
        tz_offset:

    Returns:

    """
    int_offset = int(tz_offset)
    int_hours = int(int_offset / 100)
    int_minutes = int(int_offset % 100)

    return (int_hours * 60) + int_minutes


def convert_tz_offset_to_tz_seconds(tz_offset):
    """Convert timezone offset to seconds.

    Args:
        tz_offset:

    Returns:

    """
    int_offset = int(tz_offset)
    int_hours = int(int_offset / 100)
    int_minutes = int(int_offset % 100)

    return (int_hours * 3600) + (int_minutes * 60)


def convert_tz_abbrev_to_tz_hours(tz_abbrev):
    """Get timezone offset in hours using timezone abbreviation.

    Args:
        tz_abbrev:

    Returns:

    """
    tz_offset = convert_tz_abbrev_to_tz_offset(tz_abbrev)
    return convert_tz_offset_to_tz_hours(tz_offset)


def convert_tz_abbrev_to_tz_seconds(tz_abbrev):
    """Get timezone offset in seconds using timezone abbreviation.

    Args:
        tz_abbrev:

    Returns:

    """
    tz_offset = convert_tz_abbrev_to_tz_offset(tz_abbrev)
    return convert_tz_offset_to_tz_seconds(tz_offset)


def parse_gmt_offset_timezone(tz_gmt_offset_name):
    """Parse example '(GMT-08:00) Pacific Time'
    """
    tz_parts = tz_gmt_offset_name.split(' ', 1)
    map(str.strip, tz_parts)

    tz_offset = tz_parts[0][4:-1].replace(':', '')
    tz_name = tz_parts[1]

    return tz_name, tz_offset


def validate_tz_name(tz_name):
    """Validate timezone name.
    """
    if not tz_name:
        raise ValueError("Parameter 'tz_name' is undefined.")

    if tz_name in pytz.common_timezones:
        return True

    return False


def validate_tz_abbrev(tz_abbrev):
    """Validate timezone abbreviation.
    """
    if not tz_abbrev:
        raise ValueError("Parameter 'tz_abbrev' is undefined.")

    for _tz_name in pytz.common_timezones:
        _timezone = dtz.gettz(_tz_name)
        now = dt.datetime.now(_timezone)

        _tz_abbrev = now.strftime('%Z')
        if tz_abbrev != _tz_abbrev:
            continue

        return True

    return False
