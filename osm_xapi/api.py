# -*- coding: utf-8 -*-
# !/bin/env python

import datetime
import os
import urllib2
from xml.dom import minidom

from exceptions import NonExistingData
from utils.files_manager import FileManager, GeoProvider
from utils.geo_manager import GeoManager


class API(object):
    def __init__(self):
        self.base_url = "http://overpass.osm.rambler.ru/cgi/xapi_meta"

    @classmethod
    def read_xml(cls, xml):
        dom = minidom.parseString(xml)
        # TODO
        return {}

    @classmethod
    def get_city_bbox(cls, city_name, country_code, area_size):
        countries = list(GeoProvider.iterate_supported_countries())
        if country_code not in countries:
            raise NonExistingData("No data for country_code=%s" % str(country_code))
        try:
            city = GeoProvider.iterate_city_by_name(country_code, city_name).next()
            lon, lat = float(city['lon']), float(city['lat'])
        except StopIteration:
            raise NonExistingData("City %s not supported for country=%s" % (city_name, country_code))
        return GeoManager.boundingBox(lat, lon, area_size / 2.)

    def call_api(self, min_lat, min_lon, max_lat, max_lon):
        url = "%s?way[highway=*][bbox=%s]" % (self.base_url, ','.join(map(str, [min_lat, min_lon, max_lat, max_lon])))
        res = urllib2.urlopen(url)
        return self.read_xml(res.read())

    def call_api_city(self, city_name, country_code, area_size):
        min_lat, min_lon, max_lat, max_lon = self.get_city_bbox(city_name, country_code, area_size)
        return self.call_api(min_lat, min_lon, max_lat, max_lon)


class BackupAPI(API):
    def __init__(self, backup_path):
        super(BackupAPI, self).__init__()
        self.backup_path = backup_path

    def get_file_name(self, name=None, _json=False, compressed=False, **kwargs):
        name = name if name else "%s#%s" % (
            datetime.datetime.now().strftime("%Y%m%d"),
            "#".join(map(lambda e: "%s=%s" % map(str, e), kwargs.iteritems()))
        )
        path = os.path.join(self.backup_path, name)
        path = "%s.json" % path if _json is True else path
        path = "%s.gz" % path if compressed is True else path
        return path

    @FileManager.get_data_from_file
    @FileManager.write_data_to_file
    def call_api(self, min_lat, min_lon, max_lat, max_lon):
        super(BackupAPI, self).call_api()
