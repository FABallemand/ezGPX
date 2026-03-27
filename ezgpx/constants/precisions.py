"""
This module contains constants related to precision.
"""

DEFAULT_PRECISION = 10
DEFAULT_PRECISION_DICT = {
    "lat_lon": DEFAULT_PRECISION,
    "elevation": DEFAULT_PRECISION,
    "distance": DEFAULT_PRECISION,
    "duration": DEFAULT_PRECISION,
    "speed": DEFAULT_PRECISION,
    "rate": DEFAULT_PRECISION,
    "default": DEFAULT_PRECISION,
}
POSSIBLE_TIME_FORMATS = ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"]
DEFAULT_TIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
