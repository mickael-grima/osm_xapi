
import math


class GeoManager(object):
    # Semi-axes of WGS-84 geoidal reference
    WGS84_a = 6378137.0  # Major semiaxis [m]
    WGS84_b = 6356752.3  # Minor semiaxis [m]

    @classmethod
    def deg_to_rad(cls, degrees):
        """
        degrees to radians

        :param degrees: float
        :return: float
        """
        return math.pi * degrees / 180.0

    @classmethod
    def rad_to_deg(cls, radians):
        """
        radians to degrees

        :param radians: float
        :return: float
        """
        return 180.0 * radians / math.pi

    @classmethod
    def WGS84_earth_radius(cls, lat):
        """
        Earth radius at a given latitude, according to the WGS-84 ellipsoid [m]

        :param lat: latitude (float)
        :return: float
        """
        # http://en.wikipedia.org/wiki/Earth_radius
        an = cls.WGS84_a * cls.WGS84_a * math.cos(lat)
        bn = cls.WGS84_b * cls.WGS84_b * math.sin(lat)
        ad = cls.WGS84_a * math.cos(lat)
        bd = cls.WGS84_b * math.sin(lat)
        return math.sqrt((an*an + bn*bn)/(ad*ad + bd*bd))

    @classmethod
    def boundingBox(cls, lat_deg, lon_deg, area_size):
        """
        Bounding box surrounding the point at given coordinates,
        assuming local approximation of Earth surface as a sphere
        of radius given by WGS84

        :param lat_deg: latitude in degree (float)
        :param lon_deg: longitude in degree (float)
        :param area_size: boundingbox's area's size in kilometer (float)
        :return: a tuple: minimum latitude, minimum lontitude, maximum latitude, maximum longitude
        """
        lat = cls.deg_to_rad(lat_deg)
        lon = cls.deg_to_rad(lon_deg)
        half_side = 500 * area_size

        # Radius of Earth at given latitude
        radius = cls.WGS84_earth_radius(lat)
        # Radius of the parallel at given latitude
        pradius = radius * math.cos(lat)

        lat_min = lat - half_side/radius
        lat_max = lat + half_side/radius
        lon_min = lon - half_side/pradius
        lon_max = lon + half_side/pradius

        return map(cls.rad_to_deg, [lat_min, lon_min, lat_max, lon_max])
