# -*- coding: utf-8 -*-
from django.conf.urls import url
from yandex_maps.views import yandex_map

urlpatterns = [
    url(r'^map/(?P<map_id>\d+)/$', yandex_map, name='yandex_map'),
]
