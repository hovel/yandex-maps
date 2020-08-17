# coding: utf-8
from __future__ import unicode_literals

"""
Yandex.Maps API wrapper
"""
import json
from six import text_type, binary_type
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import urlopen

STATIC_MAPS_URL = 'https://static-maps.yandex.ru/1.x/?'
HOSTED_MAPS_URL = 'https://maps.yandex.ru/?'
GEOCODE_URL = 'https://geocode-maps.yandex.ru/1.x/?'


def _format_point(longitude, latitude):
    return '%0.7f,%0.7f' % (float(longitude), float(latitude),)


def get_map_url(longitude, latitude, zoom, width, height):
    """ returns URL of static yandex map """
    point = _format_point(longitude, latitude)
    params = [
        'll=%s' % point,
        'size=%d,%d' % (width, height,),
        'z=%d' % zoom,
        'l=map',
        'pt=%s' % point
    ]
    return STATIC_MAPS_URL + '&'.join(params)


def get_external_map_url(longitude, latitude, zoom=14):
    """ returns URL of hosted yandex map """
    point = _format_point(longitude, latitude)
    params = dict(
        ll=point,
        pt=point,
        l='map',
    )
    if zoom is not None:
        params['z'] = zoom
    return HOSTED_MAPS_URL + urlencode(params)


def geocode(address, timeout=2):
    """ returns (longtitude, latitude,) tuple for given address """
    try:
        json_data = _get_geocode_json(address, timeout)
        return _get_coords(json_data)
    except IOError:
        return None, None


def _get_geocode_json(address, timeout=2):
    url = _get_geocode_url(address)
    response = urlopen(url, timeout=timeout).read()
    return response


def _get_geocode_url(address):
    if isinstance(address, text_type):
        address = address.encode('utf8')
    params = urlencode({'geocode': address, 'format': 'json', 'results': 1})
    return GEOCODE_URL + params


def _get_coords(response):
    if isinstance(response, binary_type):
        response = response.decode('utf8')
    try:
        geocode_data = json.loads(response)
        pos_data = geocode_data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        return tuple(pos_data.split())
    except (IndexError, KeyError):
        return None, None
