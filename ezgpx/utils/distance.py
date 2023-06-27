import math as m
import logging

# latitude/longitude in GPX files is always in WGS84 datum
# WGS84 defined the Earth semi-major axis with 6378.137 km
# https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
EARTH_RADIUS = 6378.137 * 1000

def haversine_distance(latitude_1: float, longitude_1: float, latitude_2: float, longitude_2: float) -> float:
    """
    Compute Haversine distance between to points.
    https://en.wikipedia.org/wiki/Haversine_formula

    Args:
        latitude_1 (float): Latitude of the first point.
        longitude_1 (float): Longitude of the first point.
        latitude_2 (float): Latitude of the second point.
        longitude_2 (float): Longitude of the second point.

    Returns:
        float: Haversine distance between the points.
    """
    # Delta and conversion to radians
    delta_lat = m.radians(latitude_1 - latitude_2)
    delta_long = m.radians(longitude_1 - longitude_2)

    sin_1 = m.sin(delta_lat/2)
    sin_2 = m.sin(delta_long/2)
    a = m.sqrt(sin_1 * sin_1 + m.cos(latitude_1) * m.cos(latitude_2) * sin_2 * sin_2)
    d = 2 * EARTH_RADIUS * m.asin(a)

    return d

def perpendicular_distance(start_point, end_point, point):
    """
    Distance between a point and a line.

    Args:
        start_point (TrackPoint): A point on the line.
        end_point (TrackPoint): A point on the line.
        point (TrackPoint): A point to measure the distance from.

    Returns:
        float: Perpendicular distance between the point *point* and the line defined by *start_point* and *end_point*.
    """

    def line_coefficients(point_1, point_2):
        """
        Compute the coefficients of a line equation of the form: ax+by+c=0.

        Args:
            point_1 (TrackPoint): A point on the line.
            point_2 (TrackPoint): A point on the line.

        Returns:
            tuple: Coefficients of the line equation.
        """
        delta_x = point_1.longitude - point_2.longitude
        delta_y = point_1.latitude - point_2.latitude
        try:
            a = delta_y / delta_x
            b = -1
            c = point_1.latitude - a * point_1.longitude
        except:
            a = 1
            b = 0
            c = point_1.longitude  
            logging.warning("Vertical line")
            
        return a, b, c

    a, b, c = line_coefficients(start_point, end_point)

    d = abs(a*point.longitude + b*point.latitude + c) / m.sqrt(a*a + b*b)
    logging.info(f"perpendicular_distance = {d}")
    return d
