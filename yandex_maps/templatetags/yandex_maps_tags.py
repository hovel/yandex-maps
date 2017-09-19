# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import template
from django.utils.html import conditional_escape, format_html
from django.utils.safestring import mark_safe

from yandex_maps.models import MapAndAddress, get_static_map_url
from yandex_maps.api import get_external_map_url

try:
    from django.contrib.gis.geos import Point
except ImportError:
    class Point(object):
        pass

register = template.Library()

# FIXME: этот код ужасен :)


def _url_for(address, external, *args, **kwargs):
    if isinstance(address, Point):
        if external:
            return get_external_map_url(address.x, address.y, *args, **kwargs)
        else:
            return get_static_map_url(address.x, address.y, *args, **kwargs)

    if not isinstance(address, MapAndAddress):
        address, created = MapAndAddress.objects.get_or_create(address=address)
    try:
        if external:
            return address.get_external_map_url(*args, **kwargs)
        else:
            return address.get_map_url(*args, **kwargs)
    except Exception:
        return ''


@register.filter
def static_map_url(address, params=None):
    '''Фильтр, который возвращает URL картинки с картой.
    Можно применять к объекту класса MapAndAddress, к строке с адресом
    или к экземпляру Point из GeoDjango (например, PointField с координатами).

    Параметры: ширина, высота, уровень детализации - через запятую без пробелов.

    Пример:

        <img src='{{ address|static_map_url:"300,200" }}'>

    '''
    data = [] if params is None else params.split(",")
    return _url_for(address, False, *data)


@register.filter
def external_map_url(address, zoom=None):
    '''Фильтр, который возвращает URL карты у яндекса.
    Можно применять к объекту класса MapAndAddress, к строке с адресом
    или к экземпляру Point из GeoDjango (например, PointField с координатами).

    Принимает 1 необязательный параметр: уровень детализации.

    Пример:

        <a href='{{ address|external_map_url }}' target='_blank'>посмотреть карту</a>

    '''
    return _url_for(address, True, zoom)


@register.simple_tag
def yandex_map(address, width, height, zoom=14, attrs=''):
    '''Тег, который выводит <img> с картой.

    Параметры:

        1. адрес (строка с адресом, объект класса MapAndAddress или Point из GeoDjango)
        2. ширина
        3. высота
        4. уровень детализации (по умолчанию = 14)

    Пример:

        {% yandex_map "Санкт-Петербург, ул. Бумажная 4" 300 200 8 %}

    '''
    url = _url_for(address, False, width, height, zoom)
    return format_html("<img src='{}' width='{}' height='{}' alt='{}' {} />",
                       url, width, height, conditional_escape(address),
                       mark_safe(attrs))
