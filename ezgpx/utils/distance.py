import math as m

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

