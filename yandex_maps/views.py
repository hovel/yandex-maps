# -*- coding: utf-8 -*-
from __future__ import absolute_import

from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from yandex_maps.models import MapAndAddress

def yandex_map(request, map_id):
    map = get_object_or_404(MapAndAddress, id=map_id)
    ctx = {
        'longitude': map.longitude,
        'latitude': map.latitude,
        'zoom': 15,
        'address': map.address,
    }
    return render_to_response('yandex_maps/map.html', ctx)
