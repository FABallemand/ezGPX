import math as m
import logging

# latitude/longitude in GPX files is always in WGS84 datum
# WGS84 defined the Earth semi-major axis with 6378.137 km
# https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
EARTH_RADIUS = 6378.137 * 1000

def haversine_distance(point_1, point_2) -> float:
    """
    Compute Haversine distance (meters) between to points.
    https://en.wikipedia.org/wiki/Haversine_formula

    Args:
        point_1 (TrackPoint): First point.
        point_2 (TrackPoint): Second point.

    Returns:
        float: Haversine distance between the points.
    """
    # Delta and conversion to radians
    delta_lat = m.radians(point_1.latitude - point_2.latitude)
    delta_long = m.radians(point_1.longitude - point_2.longitude)

    sin_1 = m.sin(delta_lat/2)
    sin_2 = m.sin(delta_long/2)
    a = m.sqrt(sin_1 * sin_1 + m.cos(m.radians(point_1.latitude)) * m.cos(m.radians(point_2.latitude)) * sin_2 * sin_2)
    d = 2 * EARTH_RADIUS * m.asin(a)

    return d

def distance(point_1, point_2) -> float:
    """
    Euclidian distance between two points.

    Args:
        point_1 (TrackPoint): First point.
        point_2 (TrackPoint): Second point.

    Returns:
        float: Distance between the points.
    """
    delta_lat = point_1.latitude - point_2.latitude
    delta_long = point_1.longitude - point_2.longitude
    return m.sqrt(delta_lat*delta_lat + delta_long*delta_long)


def perpendicular_distance(start_point, end_point, point) -> float:
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
    
    return d
