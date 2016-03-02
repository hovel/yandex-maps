# -*- coding: utf-8 -*-
from unittest import TestCase
from yandex_maps.api import _get_coords, get_map_url, geocode

RESPONSE = u"""
{"response":
     {"GeoObjectCollection":
          {"metaDataProperty": {"GeocoderResponseMetaData": {"request": "Москва", "found": "38", "results": "1"}},
           "featureMember": [
               {"GeoObject": {"metaDataProperty": {
                   "GeocoderMetaData": {"kind": "locality", "text": "Россия, Москва", "precision": "other",
                                        "AddressDetails": {
                                            "Country": {"AddressLine": "Москва", "CountryNameCode": "RU",
                                                        "CountryName": "Россия",
                                                        "Locality": {"LocalityName": "Москва"}}}}},
                              "description": "Россия", "name": "Москва",
                              "boundedBy": {"Envelope":
                                                {"lowerCorner": "37.182743 55.490667",
                                                 "upperCorner": "37.964969 56.01074"}},
                              "Point": {"pos": "37.620393 55.75396"}}}]}}}
""".encode('utf8')

UNKNOWN_ADDRESS = u'''
{"response":
     {"GeoObjectCollection": {
         "metaDataProperty": {
             "GeocoderResponseMetaData":
                 {"request": "cantfindthisaddress", "found": "0", "results": "1"}},
         "featureMember": []}}}
'''.encode('utf8')

COORDS = (u'37.620393', u'55.75396')
MAP_URL = 'http://static-maps.yandex.ru/1.x/?ll=37.6203930,55.7539600&size=200,300&z=5&l=map&pt=37.6203930,55.7539600'


class GeocodeTest(TestCase):
    def test_geocode(self):
        pos = geocode("Москва")
        self.assertEqual(pos, (COORDS[0], COORDS[1]))

    def test_parsing(self):
        self.assertEqual(_get_coords(RESPONSE), COORDS)

    def test_unknown(self):
        self.assertEqual(_get_coords(UNKNOWN_ADDRESS), (None, None,))


# FIXME: тест полагается на порядок параметров в url
class MapUrlTest(TestCase):
    def test_map_url(self):
        url = get_map_url(COORDS[0], COORDS[1], 5, 200, 300)
        self.assertEqual(url, MAP_URL)
