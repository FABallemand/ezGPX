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
        point_1 (WayPoint): First point.
        point_2 (WayPoint): Second point.

    Returns:
        float: Haversine distance between the points.
    """
    # Delta and conversion to radians
    delta_lat = m.radians(point_1.lat - point_2.lat)
    delta_long = m.radians(point_1.lon - point_2.lon)

    sin_1 = m.sin(delta_lat/2)
    sin_2 = m.sin(delta_long/2)
    a = m.sqrt(sin_1 * sin_1 + m.cos(m.radians(point_1.lat)) * m.cos(m.radians(point_2.lat)) * sin_2 * sin_2)
    d = 2 * EARTH_RADIUS * m.asin(a)

    return d

def distance(point_1, point_2) -> float:
    """
    Euclidian distance between two points.

    Args:
        point_1 (WayPoint): First point.
        point_2 (WayPoint): Second point.

    Returns:
        float: Distance between the points.
    """
    delta_lat = point_1.lat - point_2.lat
    delta_long = point_1.lon - point_2.lon
    return m.sqrt(delta_lat*delta_lat + delta_long*delta_long)


def perpendicular_distance(start_point, end_point, point) -> float:
    """
    Distance between a point and a line.

    Args:
        start_point (WayPoint): A point on the line.
        end_point (WayPoint): A point on the line.
        point (WayPoint): A point to measure the distance from.

    Returns:
        float: Perpendicular distance between the point *point* and the line defined by *start_point* and *end_point*.
    """

    def line_coefficients(point_1, point_2):
        """
        Compute the coefficients of a line equation of the form: ax+by+c=0.

        Args:
            point_1 (WayPoint): A point on the line.
            point_2 (WayPoint): A point on the line.

        Returns:
            tuple: Coefficients of the line equation.
        """
        delta_x = point_1.lon - point_2.lon
        delta_y = point_1.lat - point_2.lat

        try:
            a = delta_y / delta_x
            b = -1
            c = point_1.lat - a * point_1.lon
        except:
            a = 1
            b = 0
            c = point_1.lon  
            logging.debug("Vertical line")
            
        return a, b, c

    a, b, c = line_coefficients(start_point, end_point)

    d = abs(a*point.lon + b*point.lat + c) / m.sqrt(a*a + b*b)
    
    return d
