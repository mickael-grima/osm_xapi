# -*- coding: utf-8 -*-
# !/bin/env python

import json
import os
import gzip


class FileManager(object):
    @classmethod
    def exists_data(cls, file_name):
        return os.path.exists(file_name)

    @classmethod
    def read(cls, path, format="json"):
        with open(path, "r") as f:
            if format == "json":
                return json.load(f)
            return '\n'.join(f.readlines())

    @classmethod
    def ensure_dir(cls, file_name):
        d = os.path.dirname(file_name)
        if not os.path.exists(d):
            os.makedirs(d)

    @classmethod
    def write(cls, file_name, text, _json=False):
        cls.ensure_dir(file_name)
        with open(file_name, "w") as f:
            json.dump(text, f) if _json is True else f.write(text)

    @classmethod
    def get_data_from_file(cls, func):
        def get_data(self, *args, **kwargs):
            file_name = self.get_file_name(*args[1:], **kwargs)
            if cls.exists_data(file_name):
                data = cls.read(file_name)
                return data
            return func(self, *args, **kwargs)
        return get_data

    @classmethod
    def write_data_to_file(cls, func):
        def write_data(self, *args, **kwargs):
            data = func(self, *args, **kwargs)
            file_name = self.get_file_name(*args[1:], **kwargs)
            cls.write(file_name, data, _json=True)
            return data
        return write_data


class GeoProvider(object):
    __CITIES_PATH = os.path.abspath(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "cities")
    )

    @classmethod
    def iterate_supported_countries(cls):
        for country in os.listdir(cls.__CITIES_PATH):
            if os.path.isdir(os.path.join(cls.__CITIES_PATH, country)):
                yield country

    @classmethod
    def iterate_main_cities(cls, country):
        path = os.path.join(cls.__CITIES_PATH, country, "main_cities.json.gz")
        with gzip.open(path, "r") as f:
            for city in json.load(f):
                yield city

    @classmethod
    def iterate_main_cities_name(cls, country):
        for city in cls.iterate_main_cities(country):
            yield city["city"]

    @classmethod
    def iterate_cities(cls, country):
        path = os.path.join(cls.__CITIES_PATH, country, "cities.json.gz")
        with gzip.open(path, "r") as f:
            for city in json.load(f):
                yield city

    @classmethod
    def iterate_cities_name(cls, country):
        for city in cls.iterate_cities(country):
            yield city["city"]

    @classmethod
    def iterate_city_by_name(cls, country, *city_names):
        for city in cls.iterate_cities(country):
            if city["city"] in city_names:
                yield city
