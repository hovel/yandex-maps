# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import mock
from django.urls import reverse
from django.test import TestCase

class YandexMapTest(TestCase):
    fixtures=['yandex_maps']

    def _check_url(self, url_name, status=200, **kwargs):
        url = reverse(url_name, kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status)
        return response

    def test_nonexistant_map(self):
        self._check_url('yandex_map', 404, map_id=4)

    def test_existant_map(self):
        self._check_url('yandex_map', map_id=1)

    @mock.patch('yandex_maps.api.geocode')
    def test_tags_and_filters(self, geocode):
        geocode.return_value = '60.611084', '56.834545'
        response = self._check_url('index')
        assert response.content.count(b"src='https://static-maps.yandex.ru/1.x/?ll=60.6110840,56.8345450") == 2, response
