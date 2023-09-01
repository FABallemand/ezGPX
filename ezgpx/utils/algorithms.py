from typing import List
import logging
from math import degrees

from .distance import EARTH_RADIUS, perpendicular_distance

def ramer_douglas_peucker(points: List, epsilon: float = degrees(2/EARTH_RADIUS)):
    """
    Simplify a curve using the Ramer-Douglas-Peucker algorithm.
    Source: https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm

    Parameters
    ----------
    points : List
        List of points defining the track to simplify.
    epsilon : float, optional
        Ramer-Douglas-Peucker threshold distance (higher value means more simplifications), by default degrees(2/EARTH_RADIUS) (ie: the angle corresponding to a distance of 2 meters at the surface of the earth).

    Returns
    -------
    List
        List of points defining the simplified track.
    """
    # Find the point with the maximum distance
    d_max = 0
    i_max = 0

    start_point = points[0]
    end_point = points[len(points)-1]

    for i in range(1, len(points)-1):
        d = perpendicular_distance(start_point, end_point, points[i])
        if d > d_max:
            d_max = d
            i_max = i

    # logging.info(f"i_max = {i_max} | d_max = {d_max}")

    result = []

    # If max distance is greater than epsilon, recursively simplify
    if d_max > epsilon:
        # Recursive call
        result_1 = ramer_douglas_peucker(points[0:i_max+1], epsilon)
        result_2 = ramer_douglas_peucker(points[i_max: len(points)], epsilon)

        # Build result list
        result = result_1 + result_2[1:]
    else:
        result = [start_point, end_point]

    return result