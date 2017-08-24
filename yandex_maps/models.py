# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from yandex_maps import api


def get_static_map_url(longitude, latitude, width=None, height=None, detail_level=14):
    """
    Возвращает адрес статичной карты с учетом настроек в settings.py
    """
    w = int(width) if width else settings.YANDEX_MAPS_W
    h = int(height) if height else settings.YANDEX_MAPS_H
    detail_level = int(detail_level)
    return api.get_map_url(longitude, latitude, detail_level, w, h)


class MapAndAddress(models.Model):
    address = models.CharField(verbose_name='Адрес', max_length=255, blank=True, db_index=True)
    longitude = models.FloatField(verbose_name='Долгота', null=True, blank=True)
    latitude = models.FloatField(verbose_name='Широта', null=True, blank=True)

    def get_detail_level(self):
        return 5

    def get_map_url(self, width=None, height=None, detail_level=5):
        return get_static_map_url(self.longitude, self.latitude, width, height, detail_level)

    def get_external_map_url(self, detail_level=14):
        return api.get_external_map_url(self.longitude, self.latitude, detail_level)

    def fill_geocode_data(self):
        self.longitude, self.latitude = api.geocode(self.address)

    def save(self, *args, **kwargs):
        # fill geocode data if it is unknown
        if self.pk or (self.longitude is None) or (self.latitude is None):
            self.fill_geocode_data()
        super(MapAndAddress, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.address
