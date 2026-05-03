"""
This module contains utility functions for distances.
"""

import math as m
import warnings
from dataclasses import dataclass
from typing import Protocol, Tuple

# latitude/longitude in GPX files is always in WGS84 datum
# WGS84 defined the Earth semi-major axis with 6378.137 km
# https://en.wikipedia.org/wiki/World_Geodetic_System#WGS84
EARTH_RADIUS = 6_378_137


@dataclass
class LatLon(Protocol):
    """Protocol for latitude and longitude objects."""

    value: float


@dataclass
class HasLatLon(Protocol):
    """Protocol for objects that have latitude and longitude."""

    lat: LatLon
    lon: LatLon


def haversine_distance(point_1: HasLatLon, point_2: HasLatLon) -> float:
    """
    Compute Haversine distance (in meters) between to points.
    Source: https://en.wikipedia.org/wiki/Haversine_formula

    Args:
        point_1 (HasLatLon): First point.
        point_2 (HasLatLon): Second point.

    Returns:
        float: Haversine distance between the points.
    """
    # Delta and conversion to radians
    delta_lat = m.radians(point_1.lat.value - point_2.lat.value)
    delta_long = m.radians(point_1.lon.value - point_2.lon.value)

    sin_1 = m.sin(delta_lat / 2)
    sin_2 = m.sin(delta_long / 2)
    a = m.sqrt(
        sin_1 * sin_1
        + m.cos(m.radians(point_1.lat.value))
        * m.cos(m.radians(point_2.lat.value))
        * sin_2
        * sin_2
    )
    d = 2 * EARTH_RADIUS * m.asin(a)

    return d


def perpendicular_distance(
    start_point: HasLatLon, end_point: HasLatLon, point: HasLatLon
) -> float:
    """
    Compute perpendicular distance between a point and a line.

    Args:
        start_point (HasLatLon): A point on the line.
        end_point (HasLatLon): A point on the line.
        point (HasLatLon): A point to measure the distance from.

    Returns:
        float: Perpendicular distance between the point *point* and the
            line defined by *start_point* and *end_point*.
    """

    def line_coefficients(
        point_1: HasLatLon, point_2: HasLatLon
    ) -> Tuple[float, float, float]:
        """
        Compute the coefficients of a line equation of the form: ax+by+c=0.

        Args:
            point_1 (HasLatLon): A point on the line.
            point_2 (HasLatLon): A point on the line.
        Returns:
            Tuple[float, float, float]: Coefficients of the line equation.
        """
        delta_x = point_1.lon.value - point_2.lon.value
        delta_y = point_1.lat.value - point_2.lat.value

        try:
            a = delta_y / delta_x
            b = -1
            c = point_1.lat.value - a * point_1.lon.value
        except ZeroDivisionError:
            a = 1
            b = 0
            c = point_1.lon.value
            warnings.warn("Vertical line")

        return a, b, c

    a, b, c = line_coefficients(start_point, end_point)

    d = abs(a * point.lon.value + b * point.lat.value + c) / m.sqrt(a * a + b * b)

    return d
